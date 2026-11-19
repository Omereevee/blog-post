import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
import requests
from flask import Flask, render_template,request
import smtplib
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor, CKEditorField
from sqlalchemy import Text

mail="testuserbob28@gmail.com"
password = 'senx stbb ryos vjnd'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['SECRET_KEY'] = '._.'
bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
ckeditor = CKEditor(app)

class BlogForm(FlaskForm):
    title = StringField('Article Title:', validators=[DataRequired()])
    subtitle = StringField('Article Subtitle:', validators=[DataRequired()])
    author = StringField('Article Author:', validators=[DataRequired()])
    img_url = StringField('Image url:', validators=[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField('Submit')

class Blog(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    subtitle:Mapped[str] = mapped_column(String(250),nullable=False)
    author:Mapped[str] = mapped_column(String(250),nullable=False)
    image_url:Mapped[str] = mapped_column(String(250),nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    date:Mapped[str] = mapped_column(String(250),nullable=False)

    def __repr__(self):
        return f'blog: {self.title}'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    all_posts = Blog.query.all()
    return render_template('index.html', posts=all_posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/new-post', methods=["GET","POST"])
def create_new_post():
    form = BlogForm()
    if request.method == 'POST':
        title = form.title.data
        subtitle = form.subtitle.data
        author = form.author.data
        image_url = form.img_url.data
        body = form.body.data
        date = datetime.datetime.now().strftime("%B %d %Y")

        new_blog = Blog(title=title,subtitle=subtitle,author=author,image_url=image_url,body=body,date=date)
        db.session.add(new_blog)
        db.session.commit()

    return render_template('new-post.html', form=form)


@app.route('/contact',methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]


        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=mail, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs="omerkumble@gmail.com",
                msg=f"{message}"
            )

        return render_template('contact.html', Title="Sent Successfully", maincontent= False)

    else:
        return render_template('contact.html', Title="Contact me", maincontent= True)

@app.route('/post/<int:id>')
def post(id):
    blog = db.get_or_404(Blog, id)
    return render_template('post.html', id=id, blog=blog)


if __name__ == "__main__":
    app.run(debug=True)


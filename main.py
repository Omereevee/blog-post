import datetime

from flask import redirect, url_for
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
    img_url:Mapped[str] = mapped_column(String(250),nullable=False)
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
        img_url = form.img_url.data
        body = form.body.data
        date = datetime.datetime.now().strftime("%B %d %Y")

        new_blog = Blog(title=title,subtitle=subtitle,author=author,img_url=img_url,body=body,date=date)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('new-post.html', form=form)


@app.route("/edit-post/<int:id>", methods=["GET", "POST"],strict_slashes=False)
def edit_post(id):
    print("edit post")
    post = db.get_or_404(Blog, id)

    # Create the form and pre-fill every field manually
    edit_form = BlogForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body
    )

    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.author = edit_form.author.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data

        db.session.commit()
        return redirect(url_for('post',id=id))
    return render_template("new-post.html", form=edit_form, is_edit=True)

@app.route('/deleted/<int:id>',methods=["GET","POST"])
def delete(id):
    with app.app_context():
        blog_to_delete = db.get_or_404(Blog, id)
        db.session.delete(blog_to_delete)
        db.session.commit()
    return render_template("index.html")


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
    form = BlogForm()
    title = form.title.data
    subtitle = form.subtitle.data
    author = form.author.data
    img_url = form.img_url.data
    body = form.body.data
    date = datetime.datetime.now().strftime("%B %d %Y")
    blog = db.get_or_404(Blog, id)
    # pay attention to this CHATGPT
    return render_template('post.html', id=id, blog=blog, title=title,subtitle=subtitle,author=author,img_url=img_url,body=body,date=date)


if __name__ == "__main__":
    app.run(debug=True)


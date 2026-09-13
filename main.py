import requests
from flask import Flask, render_template,request
import smtplib

mail="testuserbob28@gmail.com"
password = 'senx stbb ryos vjnd'

app = Flask(__name__)

@app.route('/')
def home():
    response = requests.get(
        "https://api.npoint.io/080543d2cd760c70c5df"
    )
    posts_jason = response.json()
    return render_template('index.html', posts=posts_jason)

@app.route('/about')
def about():
    return render_template('about.html')

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
    response = requests.get(
        "https://api.npoint.io/080543d2cd760c70c5df"
    )
    posts_jason = response.json()[id-1]
    return render_template('post.html', id=id, jason=posts_jason)


if __name__ == "__main__":
    app.run(debug=True)


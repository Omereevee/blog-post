import requests
from flask import Flask, render_template


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

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/post/<int:id>')
def post(id):
    response = requests.get(
        "https://api.npoint.io/080543d2cd760c70c5df"
    )
    posts_jason = response.json()[id-1]
    return render_template('post.html', id=id, jason=posts_jason)


if __name__ == "__main__":
    app.run(debug=True)


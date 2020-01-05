from flask import Flask, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
    return render_template('welcome_page.html')

if __name__ == "__main__":
    app.run()
    
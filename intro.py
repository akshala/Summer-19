from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
	return "WELCOME"

if __name__ == "__main__":
	app.run()

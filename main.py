from flask import Flask, render_template
#TODO 1: Find the template from html5up
#TODO 2: Create the server

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)

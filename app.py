from flask import Flask
from mongoengine import connect

app = Flask(__name__)

# Create a connection to the MongoDB database
connect("poodtam-mongodb", host="mongodb://localhost:27017/")


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)

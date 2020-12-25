import os
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Creates a new Flask application instance called "app".
app = Flask(__name__)
# Sets the app "MONGO_URI" config variable to the "MONGO_URI" environment variable.
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

# Creates a new PyMongo instance called "mongo" to manage the connection and queries to MongoDB.
mongo = PyMongo(app)


# Calls the function below when the route(s) below is visited by the user.
@app.route("/")
def en_index():
    return "TEST"


# Checks to see if the module name is equal to "main" so that the file can be called directly instead of from a terminal.
if __name__ == "__main__":
    app.run(debug=True)

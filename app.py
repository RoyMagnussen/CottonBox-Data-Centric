import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Creates a new Flask application instance called "app".
app = Flask(__name__)
# Sets the app "MONGO_URI" config variable to the "MONGO_URI" environment variable.
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

# Creates a new PyMongo instance called "mongo" to manage the connection and queries to MongoDB.
mongo = PyMongo(app)


def get_total_shopping_cart_items() -> int:
    """
    Retrives the total quantity of items in the shopping cart.

    Iterates through each item in the shopping cart collection and increments the `total_items` variable by the item quantity amount.

    Returns:

        int: The total quantity of items in the shopping cart collection.
    """

    total_items = 0
    for item in list(mongo.db.shopping_cart.find()):
        total_items += item["quantity"]

    return total_items


context = {
    "categories": list(mongo.db.categories.find()),
    "languages": list(mongo.db.languages.find()),
    "total_items": get_total_shopping_cart_items
}


@app.route("/")
def en_index() -> render_template:
    """
    Renders `index.html` with the provided context when the specified route(s) above are visited by the users.

    Returns:

        render_template: Renders a specified template in the templates folder with the given context.
    """
    if request.method == "GET":
        callout_closed = request.cookies.get("callout_closed")

        return render_template("en_gb/index.html", title="Home", context=context, total_items=context["total_items"](), callout_closed=callout_closed)


# Checks to see if the module name is equal to "main" so that the file can be called directly instead of from a terminal.
if __name__ == "__main__":
    app.run(debug=True)

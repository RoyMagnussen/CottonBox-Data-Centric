import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Creates a new Flask application instance called "app".
app = Flask(__name__)
# Sets the app "MONGO_URI" config variable to the "MONGO_URI" environment variable.
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")

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


def get_product_colours(category_name) -> list:
    """
    Gets all of the available colours from the products in the provided category.

    Args:
        category_name (string): The name of the category.

    Returns:
        list: A list of all the available colours.
    """
    colour_list = []
    for product in list(mongo.db.products.find({"category": category_name})):
        for colour in product["colour"]:
            if colour not in colour_list:
                colour_list.append(colour)

    return colour_list


context = {
    "categories": list(mongo.db.categories.find()),
    "languages": list(mongo.db.languages.find()),
    "total_items": get_total_shopping_cart_items,
    "latest_products": list(mongo.db.products.find().skip(mongo.db.products.estimated_document_count() - 6))
}


@app.route("/", methods=["POST", "GET"])
def en_index() -> render_template:
    """
    Renders `index.html` with the provided context when the specified route(s) above are visited by the users.

    Returns:

        render_template: Renders a specified template in the templates folder with the given context.
    """
    if request.method == "POST":
        id = request.form["productId"]
        product = mongo.db.products.find_one({"_id": ObjectId(id)})

        name = product["name"]
        price = int(product["price"])
        colour = request.form["productColourRadio"]
        size = request.form["productSizeRadio"]
        quantity = int(request.form["productQuantity"])
        total_price = int(price * quantity)

        mongo.db.shopping_cart.insert_one({"name": name, "price": price,
                                           "colour": colour, "size": size, "quantity": quantity, "total_price": total_price})

        flash(
            f"{quantity} x {name} has been successfully added into the shopping cart!")

        return redirect(url_for("en_index"))

    if request.method == "GET":
        callout_closed = request.cookies.get("callout_closed")

        return render_template("en_gb/index.html", title="Home", context=context, total_items=context["total_items"](), callout_closed=callout_closed)


# Checks to see if the module name is equal to "main" so that the file can be called directly instead of from a terminal.
if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Creates a new Flask application instance called "app".
app = Flask(__name__)

# Sets the app "MONGO_URI" config variable to the "MONGO_URI" environment variable.
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

# Sets the app secret key to the "SECRET_KEY" environment variable. This is used for flashing messages to the user.
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


def get_product_sizes(category_name) -> list:
    """
    Gets all of the available sizes from the products in the provided category.

    Args:
        category_name (string): The name of the category.

    Returns:
        list: A list of all the available sizes.
    """
    size_list = []
    for product in list(mongo.db.products.find({"category": category_name})):
        for size in product["size"]:
            if size not in size_list:
                size_list.append(size)

    return size_list


def get_product_prices(category_name) -> list:
    """
    Gets all of the available prices from the products in the provided category.

    Args:
        category_name (string): The name of the category.

    Returns:
        list: A list of all the available prices.
    """
    price_list = []
    for product in list(mongo.db.products.find({"category": category_name})):
        if product["price"] not in price_list:
            price_list.append(product["price"])

    return price_list


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
    if request.method == "GET":
        callout_closed = request.cookies.get("callout_closed")

        return render_template("en_gb/index.html", title="Home", context=context, total_items=context["total_items"](), callout_closed=callout_closed)


@app.route("/add_to_cart/", methods=["GET", "POST"])
def add_to_cart() -> redirect:
    """
    Adds the selected product into the shopping cart with the selected colour, size and quantity options.

    Returns:
        redirect: Redirects the page to the provided url once the operation has been completed.
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

        return redirect(request.referrer)


@app.route("/category/<category_name>/", methods=["GET", "POST"])
def en_category_page(category_name) -> render_template:
    """
    Renders `category_page.html` with the products from the provided category name.

    Args:
        category_name (string): The name of the category.

    Returns:
        render_template: Renders a specified template in the templates folder with the given context. 
    """

    # Collects all of the unique colours from the products in the provided category.
    colours = get_product_colours(category_name)

    # Collects all of the unique sizes from the products in the provided category.
    sizes = get_product_sizes(category_name)

    # Collects all of the unique prices from the products in the provide category.
    prices = get_product_prices(category_name)

    # Filter dictionary used for the MongoDB query.
    filter = {
        "category": category_name
    }

    if request.args:
        # Collects the selected colour options from the colour list
        colour = request.args.getlist("colour")

        # Collects the selected size options from the size list
        size = request.args.getlist("size")

        # Collects the selected price options from the price list
        price = request.args.getlist("price")

        # Checks to see if each list has more than 0 elements, if so then it will add the list to the filter dictionary.
        if len(colour) > 0:
            filter["colour"] = {"$in": colour}
        if len(size) > 0:
            filter["size"] = {"$in": size}
        if len(price) > 0:
            filter["price"] = {"$lte": int(price)}

        # Finds all of the products based on the filter dictionary
        products = list(mongo.db.products.find(filter))

        return render_template("en_gb/category_page.html", title=category_name, context=context, total_items=context["total_items"](), products=products, product_colours=colours,
                               product_sizes=sizes, product_prices=prices)

    # Finds all of the products based on the filter dictionary
    products = list(mongo.db.products.find(filter))

    return render_template("en_gb/category_page.html", title=category_name, context=context, total_items=context["total_items"](), products=products, product_colours=colours,
                           product_sizes=sizes, product_prices=prices)


# Checks to see if the module name is equal to "main" so that the file can be called directly instead of from a terminal.
if __name__ == "__main__":
    app.run(debug=True)

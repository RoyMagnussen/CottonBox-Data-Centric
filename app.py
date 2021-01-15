import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import EnContactForm, CheckoutForm

# Creates a new Flask application instance called "app".
app = Flask(__name__)

# Sets the app "MONGO_URI" config variable to the "MONGO_URI" environment variable.
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Sets the app secret key to the "SECRET_KEY" environment variable. This is used for flashing messages to the user.
app.secret_key = os.environ.get("SECRET_KEY")

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
        total_items += int(item["quantity"])

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


def get_grand_total():
    grand_total = 0
    for product in list(mongo.db.shopping_cart.find()):
        grand_total += product["total_price"]

    return grand_total


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
        cookies_accepted = request.cookies.get("cottonbox_accept")

        return render_template("en_gb/index.html", title="Home", context=context, total_items=context["total_items"](), callout_closed=callout_closed, cookies_accepted=cookies_accepted)


@app.route("/add_to_cart/", methods=["GET", "POST"])
def add_to_cart() -> redirect:
    """
    Adds the selected product into the shopping cart with the selected colour, size and quantity options.

    Returns:
        redirect: Redirects the page to the provided url once the operation has been completed.
    """
    if request.method == "POST":
        id = request.form.get("productId")
        product = mongo.db.products.find_one({"_id": ObjectId(id)})

        name = product["name"]
        price = int(product["price"])
        image_url = product["image_url"]
        colour = request.form["productColourRadio"]
        size = request.form["productSizeRadio"]
        quantity = int(request.form["productQuantity"])
        total_price = int(price * quantity)

        mongo.db.shopping_cart.insert_one({"name": name, "price": price, "id": id, "image_url": image_url,
                                           "colour": colour, "size": size, "quantity": quantity, "total_price": total_price})

        flash(
            f"{quantity} x {name} has been successfully added into the shopping cart!")

        return redirect(request.referrer)


@app.route("/remove_from_cart/", methods=["GET", "POST"])
def remove_from_cart() -> redirect:
    """
    Removes the selected product from the shopping_cart collection.

    Returns:
        redirect: Redirects the page to the provided url once the operation has been completed.
    """
    if request.method == "POST":
        product_id = request.form.get("productId")
        mongo.db.shopping_cart.delete_one({"_id": ObjectId(product_id)})
        flash("The product was successfully removed from the shopping cart!")
        return redirect(url_for('en_shopping_cart'))


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


@app.route("/category/<category_name>/<string:id>/", methods=["GET", "POST"])
def en_product_page(category_name, id) -> render_template:
    """
    Renders `product_page.html` with the specified product using the Id provided.

    Args:
        category_name (string): The name of the category the product belongs to.
        id (string): The Id of the product.

    Returns:
        render_template: Renders a specified template in the templates folder with the given context.
    """
    product = mongo.db.products.find_one({"_id": ObjectId(id)})

    return render_template("en_gb/product_page.html", title=product["name"], context=context, total_items=context["total_items"](), product=product)


@app.route("/about/")
def en_about_page() -> render_template:
    """
    Renders `about.html`when the specified url(s) above are visited by the user.

    Returns:
        render_template: RRenders a specified template in the templates folder with the given context.
    """
    context["map_api_key"] = os.environ.get("MAP_API_KEY")
    return render_template("en_gb/about_page.html", title="About Us", context=context, total_items=context["total_items"]())


@app.route("/contact/", methods=["GET", "POST"])
def en_contact_us() -> render_template:
    """
    Renders `contact_page.html` when the specified url(s) above are visited by the user.

    Returns:
        render_template: Renders a specified template in the templates folder with the given context.
    """
    form = EnContactForm()

    if request.method == "POST":
        context["email_sent"] = True
        flash("Thank you for contacting us. Your message has been sent and someone should contact you soon!")
        return render_template("en_gb/contact_page.html", title="Contact Us", context=context, total_items=context["total_items"](), form=form)

    return render_template("en_gb/contact_page.html", title="Contact Us", context=context, total_items=context["total_items"](), form=form)


@app.route("/cart/", methods=["GET", "POST"])
def en_shopping_cart() -> render_template:
    """
    Renders `shopping_cart.html` when the specified url(s) above are visited by the user.

    Displays all of the products in the shopping cart collection.

    Returns:
        render_template: Renders a specified template in the templates folder with the given context.
    """
    products = list(mongo.db.shopping_cart.find())
    context["grand_total"] = get_grand_total

    return render_template("en_gb/shopping_cart.html", title="Shopping Cart", context=context, total_items=context["total_items"](), grand_total=context["grand_total"](), products=products)


@app.route("/cart/edit/<id>", methods=["GET", "POST"])
def en_edit_shopping_cart(id) -> render_template:
    """
    Renders `edit_shopping_cart.html` when the specified url(s) above are visited by the user.

    Retrieves the selected product from the shopping_cart collection as well as the product from the products collection.

    Updates the shopping_cart collection product's details from the form generated from the products collection product's details.

    Args:
        id (string): The unique id created by MongoDB.

    Returns:
        render_template: Renders a specified template in the templates folder with the given context.
    """
    context["grand_total"] = get_grand_total
    context["edit_products"] = True

    shopping_cart_product = mongo.db.shopping_cart.find_one({"id": id})
    selected_product = mongo.db.products.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        colour = request.form["productColourRadio"]
        size = request.form["productSizeRadio"]
        quantity = int(request.form.get("productQuantity"))
        total_price = selected_product["price"] * quantity

        product_id = request.form["productId"]

        mongo.db.shopping_cart.update_one({"_id": ObjectId(product_id)}, {
                                          "$set": {"colour": colour, "size": size, "quantity": quantity, "total_price": total_price}})

        return redirect(url_for('en_shopping_cart'))

    return render_template("en_gb/edit_shopping_cart.html", title="Shopping Cart", context=context, total_items=context["total_items"](), grand_total=context["grand_total"](), shopping_cart_product=shopping_cart_product, selected_product=selected_product)


@app.route("/sitemap/")
def en_sitemap() -> render_template:
    """
    Renders `sitemap.html` when the specified url(s) above are vistied by the user.

    Returns:
        render_template: Renders a specified template in the templates folder with the given context.
    """
    return render_template("en_gb/sitemap.html", title="Sitemap", context=context, total_items=context["total_items"]())


@app.route("/cookie_policy/")
def cookie_policy_page() -> render_template:
    """
    Renders `cookie_policy.html` when the specified url(s) above are visited by the user.

    Returns:
        render_template: Renders a specified template in the templates folder with the given context.
    """
    return render_template("en_gb/cookie_policy.html", title="Cookie Policy", context=context, total_items=context["total_items"]())


@app.route("/checkout/")
def checkout() -> render_template:
    """
    Renders `checkout.html` when the specified url(s) above are visited by the user.

    Descreases the stock_quantity amount for each product in the products collection that is in the shopping_cart collection by the quntity amount.

    Returns:
        render_template: Renders a specified template in the templates folder with the given context.
    """
    form = CheckoutForm()
    if request.method == "POST":
        for product in list(mongo.db.shopping_cart.find()):
            mongo.db.products.find_one_and_update({"_id": ObjectId(product.id)}, {
                                                  "$desc": {"stock_quantity": product.quantity}})
            mongo.db.shopping_cart.delete_one({"_id": ObjectId(product._id)})

        flash("Your purchase has been successfull! We look forward to you buying from us again!")
        return redirect(url_for("en_index"))

    return render_template("en_gb/checkout.html", title="Checkout", context=context, total_items=context["total_items"](), form=form)


# Checks to see if the module name is equal to "main" so that the file can be called directly instead of from a terminal.
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"))

import unittest
from app import app
from app import mongo
from app import get_total_shopping_cart_items


class FlaskTestCase(unittest.TestCase):
    """
    Test cases for Flask and the application.

    Args:

        unittest.TestCase (class): The TestCase class from the unittest module.
    """

    def test_en_index(self):
        """
        Checks the status code for the `en_index` route function to see if the page exists.
        """
        tester = app.test_client()
        response = tester.get("/", content_type="text/html")
        self.assertEqual(response.status_code, 200)

    def test_get_total_shopping_cart_items(self):
        """
        Checks to see if the `get_total_shopping_cart_items` function returns the correct data type and value.
        """
        result = get_total_shopping_cart_items()
        self.assertEqual(type(result), int)
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()

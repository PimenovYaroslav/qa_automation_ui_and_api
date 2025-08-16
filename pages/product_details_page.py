from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.products_page import ProductsPage


class ProductDetailsPage(BasePage):
    """
    Page Object for the product details page.

    This class contains methods and locators to interact with elements
    on the page that displays detailed information about a single product.
    """

    # Locators for elements on the Product Details page
    PRODUCT_NAME = (By.XPATH, "//div[contains(@class, 'inventory_details_name')]")
    PRODUCT_DESCRIPTION = (By.XPATH, "//div[contains(@class, 'inventory_details_desc ')]")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_details_price")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart")
    BACK_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        """
        Initializes the ProductDetailsPage Page Object with the WebDriver instance.
        Calls the parent class's constructor to set up the driver and waits.
        """
        super().__init__(driver)

    def get_product_name(self):
        """
        Retrieves the name of the product from the page.

        Returns:
            str: The text content of the product name.
        """
        return self.get_element_text(self.PRODUCT_NAME)

    def get_product_price(self):
        """
        Retrieves the price of the product from the page.

        Returns:
            str: The text content of the product price (e.g., "$29.99").
        """
        return self.get_element_text(self.PRODUCT_PRICE)

    def get_product_description(self):
        """
        Retrieves the description of the product from the page.

        Returns:
            str: The text content of the product description.
        """
        return self.get_element_text(self.PRODUCT_DESCRIPTION)

    def get_all_product_details(self):
        """
        Gathers all key details of the product into a dictionary.
        This is a convenience method for tests that need to verify multiple
        attributes at once.

        Returns:
            dict: A dictionary containing the product's 'name', 'description',
                  and 'price'.
        """
        return {
            "name": self.get_product_name(),
            "description": self.get_product_description(),
            "price": self.get_product_price()
        }

    def click_back_to_products_button(self):
        """
        Clicks the "Back to products" button to navigate back to the product listing page.
        This method returns a new instance of the ProductsPage.

        Returns:
            ProductsPage: A new instance of the ProductsPage class.
        """
        self.click_element(self.BACK_BUTTON)
        return ProductsPage(self.driver)
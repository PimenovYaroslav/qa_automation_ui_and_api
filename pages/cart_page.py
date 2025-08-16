from selenium.webdriver.common.by import By
import random
from pages.base_page import BasePage
from pages.checkout_page_1 import CheckoutPageOne


class CartPage(BasePage):
    """
    Page Object for the shopping cart page.

    This class contains methods and locators for interacting with elements
    on the cart page, such as removing items, proceeding to checkout,
    and verifying the contents of the cart.
    """

    # Locators for elements on the Cart page
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CART_TITLE = (By.XPATH, "//span[@class='title' and text()='Your Cart']")
    # A dynamic locator function to find a cart item by its name
    CART_ITEM_NAME_BY_TEXT = lambda self, item_name: (
        By.XPATH, f"//div[@class='inventory_item_name' and text()='{item_name}']")
    REMOVE_CART_BUTTONS = (By.XPATH, "//button[contains(@class, 'btn_secondary') and contains (text(), 'Remove')]")
    ADDED_PRODUCTS = (By.CLASS_NAME, "inventory_item_name")
    # A relative locator to find the product name from a "Remove" button's context
    PRODUCT_NAME_FROM_ADDED_PRODUCTS = (By.XPATH, "./ancestor::div[@class='cart_item_label']//div["
                                                  "@class='inventory_item_name']")

    def __init__(self, driver):
        """
        Initializes the CartPage with the WebDriver instance.
        Calls the parent class's constructor to set up the driver and wait.
        """
        super().__init__(driver)

    def is_cart_page_displayed(self):
        """
        Checks if the cart page is currently displayed by verifying the page title.

        Returns:
            bool: True if the cart title is visible, False otherwise.
        """
        return self.is_element_displayed(self.CART_TITLE)

    def is_item_in_cart_by_name(self, item_name):
        """
        Checks if a specific item is present in the cart by its name.

        Args:
            item_name (str): The name of the item to check for.

        Returns:
            bool: True if the item is found, False otherwise.
        """
        locator = self.CART_ITEM_NAME_BY_TEXT(item_name)
        return self.is_element_displayed(locator)

    def remove_random_item_from_cart(self):
        """
        Selects a random "Remove" button and clicks it to remove an item from the cart.
        This is useful for tests that involve dynamic removal of products.

        Returns:
            str: The name of the product that was removed.
        """
        # Find all "Remove" buttons
        all_remove_buttons = self.find_elements(self.REMOVE_CART_BUTTONS)
        # Select a random button from the list
        random_remove_button = random.choice(all_remove_buttons)
        # Find the product name associated with the random button
        removed_product = random_remove_button.find_element(*self.PRODUCT_NAME_FROM_ADDED_PRODUCTS)
        removed_product_name = removed_product.text
        # Click the randomly selected remove button
        random_remove_button.click()
        return removed_product_name

    def get_cart_items_names(self):
        """
        Retrieves a list of all product names currently in the cart.

        Returns:
            list: A list of strings, where each string is the name of a product.
        """
        added_products_names = []
        # Find all elements with the class 'inventory_item_name'
        added_products_list = self.find_elements(self.ADDED_PRODUCTS)
        for product in added_products_list:
            # Get the text (name) of each product
            name = self.get_element_text(product)
            added_products_names.append(name)
        return added_products_names

    def click_checkout_button(self):
        """
        Clicks the "Checkout" button to proceed to the checkout information page.
        Asserts that the URL changes to the expected checkout page.

        Returns:
            CheckoutPageOne: A new instance of the CheckoutPageOne class.
        """
        self.click_element(self.CHECKOUT_BUTTON)
        # It's good practice to assert the state change within the page object itself
        assert self.get_current_url() == "https://www.saucedemo.com/checkout-step-one.html"
        return CheckoutPageOne(self.driver)
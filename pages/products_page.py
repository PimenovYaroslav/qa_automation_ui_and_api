import random
import re
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):
    """
    Page Object for the products listing page.

    This class handles all interactions on the main product inventory page,
    including adding/removing items, sorting, and navigating to product details.
    """

    # Locators for elements on the Products page
    PRODUCTS_TITLE = (By.XPATH, "//span[@class='title' and text()='Products']")
    ALL_PRODUCT_IMAGES = (By.XPATH, "//img[@class='inventory_item_img']")
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    ALL_PRODUCT_LIST_ADD = (By.XPATH, "//button[contains(@class, 'btn_inventory') and contains(text(), 'Add to cart')]")
    ALL_PRODUCT_LIST_REMOVE = (By.XPATH, "//button[contains(@class, 'btn_inventory') and contains(text(), 'Remove')]")
    # A relative locator to find the product name from a button's context
    PRODUCT_NAME_FROM_LIST = (By.XPATH, """
            ./ancestor::div[contains(@class,'inventory_item_description')]
            //div[contains(@class,'inventory_item_name')]
        """)
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    PRODUCTS_PRICES = (By.XPATH, "//div[@class='inventory_item_price']")
    PRODUCT_INFO_FATHER = (By.XPATH, "//div[@class='inventory_item']")
    # Relative locators for product information within a single product container
    PRODUCT_NAME_FROM_FATHER = (By.XPATH, ".//div[contains(@class, 'inventory_item_name')]")
    PRODUCT_DESCRIPTION_FROM_FATHER = (By.XPATH, ".//div[@class='inventory_item_desc']")
    PRODUCT_PRICE_FROM_FATHER = (By.XPATH, ".//div[@class='inventory_item_price']")

    def __init__(self, driver):
        """
        Initializes the ProductsPage with the WebDriver instance.
        """
        super().__init__(driver)

    def is_products_page_displayed(self):
        """
        Checks if the products page is currently displayed by verifying the title.

        Returns:
            bool: True if the "Products" title is visible, False otherwise.
        """
        return self.is_element_displayed(self.PRODUCTS_TITLE)

    def get_products_title_text(self):
        """
        Retrieves the text of the "Products" title.

        Returns:
            str: The text content of the page title.
        """
        return self.get_element_text(self.PRODUCTS_TITLE)

    def add_sauce_labs_backpack_to_cart(self):
        """
        Adds the "Sauce Labs Backpack" to the shopping cart by clicking its specific button.
        """
        self.click_element(self.ADD_BACKPACK)

    def is_add_backpack_button_displayed(self):
        """
        Checks if the "Add to cart" button for the backpack is displayed.

        Returns:
            bool: True if the button is visible, False otherwise.
        """
        return self.is_element_displayed(self.ADD_BACKPACK)

    def is_remove_backpack_button_displayed(self):
        """
        Checks if the "Remove" button for the backpack is displayed.

        Returns:
            bool: True if the button is visible, False otherwise.
        """
        return self.is_element_displayed(self.REMOVE_BACKPACK)

    def select_random_product_and_get_details(self):
        """
        Selects a random product from the list, gathers its details,
        and clicks on the product name to navigate to its details page.

        Returns:
            tuple: A tuple containing a dictionary of the product's details
                   and a new instance of the ProductDetailsPage.
        """
        from pages.product_details_page import ProductDetailsPage
        products_list = self.find_elements(self.PRODUCT_INFO_FATHER)
        random_product = random.choice(products_list)
        # Find elements relative to the chosen product's container
        name_element = random_product.find_element(*self.PRODUCT_NAME_FROM_FATHER)
        desc_element = random_product.find_element(*self.PRODUCT_DESCRIPTION_FROM_FATHER)
        price_element = random_product.find_element(*self.PRODUCT_PRICE_FROM_FATHER)
        product_data = {
            "name": name_element.text,
            "description": desc_element.text,
            "price": price_element.text
        }
        # Click the product name to navigate
        name_element.click()
        return product_data, ProductDetailsPage(self.driver)

    def add_random_products_to_cart(self):
        """
        Randomly selects and adds a number of products to the cart.

        Returns:
            int: The number of products that were added to the cart.
        """
        product_list = self.find_elements(self.ALL_PRODUCT_LIST_ADD)
        count = random.randint(1, len(product_list))
        random_products = random.sample(product_list, count)
        for product in random_products:
            product.click()
        return count

    def add_random_products_to_cart_and_get_names(self):
        """
        Adds a random number of products to the cart and returns their names.

        Returns:
            list: A list of strings, where each string is the name of an added product.
        """
        product_list = self.find_elements(self.ALL_PRODUCT_LIST_ADD)
        count = random.randint(2, len(product_list))
        random_products = random.sample(product_list, count)
        added_products_texts = []
        for product in random_products:
            # Find the product name element relative to the 'Add to cart' button
            product_name_element = product.find_element(*self.PRODUCT_NAME_FROM_LIST)
            product_name_element_text = product_name_element.text
            added_products_texts.append(product_name_element_text)
            product.click()
        return added_products_texts

    def select_sorting_products_by_value(self, value):
        """
        Selects a sorting option from the dropdown menu by its value attribute.

        Args:
            value (str): The value attribute of the sorting option (e.g., "az", "za", "lohi", "hilo").
        """
        self.select_by_value(self.SORT_SELECT, value)

    def get_products_prices(self):
        """
        Retrieves the prices of all products on the page and converts them to floats.

        Returns:
            list: A list of floats representing the prices of all products.
        """
        products_list = self.find_elements(self.PRODUCTS_PRICES)
        product_prices = []
        for product in products_list:
            text = product.text
            # Use regex to find the price (e.g., "$29.99" -> 29.99)
            price = float(re.findall(r'\d+\.\d+', text)[0])
            product_prices.append(price)
        return product_prices

    def get_count_of_add_to_cart_buttons(self):
        """
        Returns the number of "Add to cart" buttons currently visible on the page.

        Returns:
            int: The count of "Add to cart" buttons.
        """
        products_list = self.find_elements(self.ALL_PRODUCT_LIST_ADD)
        return len(products_list)

    def get_count_remove_buttons(self):
        """
        Returns the number of "Remove" buttons currently visible on the page.

        Returns:
            int: The count of "Remove" buttons.
        """
        products_list = self.find_elements(self.ALL_PRODUCT_LIST_REMOVE)
        return len(products_list)
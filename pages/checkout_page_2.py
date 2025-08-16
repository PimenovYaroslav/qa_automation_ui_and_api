from selenium.webdriver.common.by import By
import re
from pages.base_page import BasePage
from pages.checkout_complete_page import CheckoutComplete


class CheckoutPageTwo(BasePage):
    """
    Page Object for the second step of the checkout process (order overview).

    This page allows for verification of item prices, tax, and the total
    before the final order is placed.
    """

    # Locators for price summary elements on the page
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    def __init__(self, driver):
        """
        Initializes the CheckoutPageTwo Page Object with the WebDriver instance.
        Calls the parent class's constructor to set up the driver and waits.
        """
        super().__init__(driver)

    def get_item_total(self):
        """
        Retrieves the item subtotal price from the page and converts it to a float.
        Uses a regular expression to extract the numerical value from the text.

        Returns:
            float: The numerical value of the item total.
        """
        price_text = self.get_element_text(self.ITEM_TOTAL)
        # Regex to find one or more digits, a decimal point, and one or more digits
        match = re.search(r'\d+\.\d+', price_text)
        if match:
            return float(match.group(0))
        raise ValueError("Could not extract item total price from text: " + price_text)

    def get_tax(self):
        """
        Retrieves the tax amount from the page and converts it to a float.
        Uses a regular expression to extract the numerical value.

        Returns:
            float: The numerical value of the tax.
        """
        price_text = self.get_element_text(self.TAX)
        match = re.search(r'\d+\.\d+', price_text)
        if match:
            return float(match.group(0))
        raise ValueError("Could not extract tax price from text: " + price_text)

    def get_total(self):
        """
        Retrieves the final total price (item total + tax) from the page.
        Uses a regular expression to extract the numerical value.

        Returns:
            float: The numerical value of the total price.
        """
        price_text = self.get_element_text(self.TOTAL)
        match = re.search(r'\d+\.\d+', price_text)
        if match:
            return float(match.group(0))
        raise ValueError("Could not extract total price from text: " + price_text)

    def click_finish_button(self):
        """
        Clicks the "Finish" button to complete the order.
        Asserts that the URL changes to the expected checkout complete page.

        Returns:
            CheckoutComplete: A new instance of the CheckoutComplete Page Object.
        """
        self.click_element(self.FINISH_BUTTON)
        # It's good practice to assert the URL change within the page object
        assert self.get_current_url() == "https://www.saucedemo.com/checkout-complete.html"
        return CheckoutComplete(self.driver)
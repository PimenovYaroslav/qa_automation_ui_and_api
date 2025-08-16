from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutComplete(BasePage):
    """
    Page Object for the checkout complete page.

    This class contains methods and locators to interact with and verify
    the elements on the page that confirms the order is complete.
    """

    # Locators for elements on the Checkout Complete page
    THANK_YOU_TEXT = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        """
        Initializes the CheckoutComplete Page Object with the WebDriver instance.
        Calls the parent class's constructor to set up the driver and waits.
        """
        super().__init__(driver)

    def is_thank_you_displayed(self):
        """
        Checks if the "Thank you for your order!" text is displayed on the page.

        Returns:
            bool: True if the thank you text is visible, False otherwise.
        """
        return self.is_element_displayed(self.THANK_YOU_TEXT)
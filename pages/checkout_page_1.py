from selenium.webdriver.common.by import By
from faker import Faker
from pages.base_page import BasePage
from pages.checkout_page_2 import CheckoutPageTwo


class CheckoutPageOne(BasePage):
    """
    Page Object for the first step of the checkout process (customer information).

    This class handles filling out the checkout form and navigating to the
    next step of the checkout flow.
    """

    # Locators for input fields and the continue button on the checkout page
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE_BUTTON = (By.XPATH, "//h3[@data-test='error']")

    def __init__(self, driver):
        """
        Initializes the CheckoutPageOne Page Object with the WebDriver instance.
        Calls the parent class's constructor to set up the driver and waits.
        """
        super().__init__(driver)

    def generate_checkout_data(self) -> dict:
        """
        Generates a dictionary of realistic test data for the checkout form
        using the Faker library.

        Returns:
            dict: A dictionary containing 'first_name', 'last_name', and 'postal_code'.
        """
        # Initialize Faker with Ukrainian locale for realistic data
        faker = Faker('uk_UA')
        test_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "postal_code": faker.postcode()
        }
        return test_data

    def generate_checkout_data_with_empty_zip(self) -> dict:
        """
        Generates test data for an invalid scenario with an empty postal code.

        Returns:
            dict: A dictionary containing valid 'first_name' and 'last_name'
                  but an empty 'postal_code'.
        """
        faker = Faker('uk_UA')
        test_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "postal_code": ""
        }
        return test_data

    def fill_checkout_form(self, data):
        """
        Fills out the checkout form with the provided data.

        Args:
            data (dict): A dictionary containing 'first_name', 'last_name',
                         and 'postal_code'.
        """
        self.enter_text(self.FIRST_NAME_INPUT, data["first_name"])
        self.enter_text(self.LAST_NAME_INPUT, data["last_name"])
        self.enter_text(self.POSTAL_CODE_INPUT, data["postal_code"])

    def click_continue_button(self):
        """
        Clicks the "Continue" button to proceed to the next step.
        It handles two possible outcomes: either the next page loads,
        or an error message is displayed (for validation failures).

        Returns:
            BasePage or CheckoutPageTwo: An instance of CheckoutPageTwo if
                                         successful, or the current page object
                                         (self) if an error occurs.
        """
        self.click_element(self.CONTINUE_BUTTON)
        # Check if an error message is displayed after clicking continue
        if self.is_error_message_displayed():
            # If so, return the current page object for further validation
            return self
        else:
            # Otherwise, return the next page object
            return CheckoutPageTwo(self.driver)

    def is_error_message_displayed(self):
        """
        Checks if the error message element is visible on the page.

        Returns:
            bool: True if the error message is displayed, False otherwise.
        """
        return self.is_element_displayed(self.ERROR_MESSAGE_BUTTON)

    def get_error_message_text(self):
        """
        Retrieves the text of the validation error message.

        Returns:
            str: The text content of the error message.
        """
        return self.get_element_text(self.ERROR_MESSAGE_BUTTON)
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object for the login page.

    This class contains methods and locators for interacting with elements
    on the login page, such as inputting credentials and clicking the login button.
    """

    # Locators for elements on the Login page
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")
    LOGIN_BOX = (By.CLASS_NAME, "login-box")

    def __init__(self, driver):
        """
        Initializes the LoginPage with the WebDriver instance.
        Calls the parent class's constructor to set up the driver and waits.
        """
        super().__init__(driver)

    def login(self, username, password):
        """
        Performs a login action by entering a username and password
        and then clicking the login button.

        Args:
            username (str): The username to enter.
            password (str): The password to enter.
        """
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self):
        """
        Retrieves the text of the error message displayed on the login page.
        This is useful for verifying failed login attempts.

        Returns:
            str: The text content of the error message.
        """
        return self.get_element_text(self.ERROR_MESSAGE)

    def id_login_box_visible(self):
        """
        Checks if the main login container box is displayed on the page.
        This can be used to verify that the user is on the login page.

        Returns:
            bool: True if the login box is visible, False otherwise.
        """
        return self.is_element_displayed(self.LOGIN_BOX)
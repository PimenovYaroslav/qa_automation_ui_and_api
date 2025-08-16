from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select


class BasePage:
    """
    A base class for all Page Objects.

    This class provides common methods and attributes that are shared across
    multiple pages, such as interacting with a browser, waiting for elements,
    and handling common UI components like the shopping cart and burger menu.
    This approach follows the Page Object Model (POM) design pattern, promoting
    reusability and maintainability of UI tests.
    """

    # Locators for common UI elements that are present on multiple pages
    SHOPPING_CART_ICON = (By.ID, "shopping_cart_container")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    BURGER_MENU_ICON = (By.ID, "react-burger-menu-btn")
    BURGER_LOGOUT = (By.ID, "logout_sidebar_link")
    BURGER_MENU_WRAPPER = (By.CLASS_NAME, "bm-menu-wrap")
    BURGER_MENU_RESET = (By.ID, "reset_sidebar_link")
    BURGER_MENU_CLOSE = (By.ID, "react-burger-cross-btn")

    def __init__(self, driver):
        """
        Initializes the BasePage with a WebDriver instance.

        Args:
            driver: The Selenium WebDriver instance.
        """
        self.driver = driver
        # Initialize WebDriverWait with a 10-second timeout for explicit waits
        self.wait = WebDriverWait(driver, 10)

    def open_url(self, url):
        """
        Navigates the browser to a specific URL.

        Args:
            url (str): The URL to open.
        """
        self.driver.get(url)

    def find_element(self, locator):
        """
        Waits for and returns a single element to be visible on the page.

        Args:
            locator (tuple): A tuple containing the locator strategy (e.g., By.ID)
                             and the locator value.

        Returns:
            WebElement: The found web element.
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        """
        Waits for and returns a list of elements to be visible on the page.

        Args:
            locator (tuple): A tuple containing the locator strategy and value.

        Returns:
            list[WebElement]: A list of found web elements.
        """
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click_element(self, locator):
        """
        Waits for an element to be clickable and then clicks it.

        Args:
            locator (tuple): A tuple containing the locator strategy and value.
        """
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text):
        """
        Finds an element, clears its current value, and then enters the given text.

        Args:
            locator (tuple): A tuple containing the locator strategy and value.
            text (str): The text to be entered into the element.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, element_or_locator) -> str:
        """
        Gets the visible text from a web element or a locator.

        Args:
            element_or_locator (WebElement or tuple): The element itself or its locator.

        Returns:
            str: The text content of the element.
        """
        if isinstance(element_or_locator, WebElement):
            return element_or_locator.text
        elif isinstance(element_or_locator, tuple) and len(element_or_locator) == 2:
            element = self.find_element(element_or_locator)
            return element.text

    def is_element_displayed(self, locator):
        """
        Checks if an element is displayed on the page without failing the test
        if the element is not found.

        Args:
            locator (tuple): A tuple containing the locator strategy and value.

        Returns:
            bool: True if the element is displayed, False otherwise.
        """
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False

    def wait_for_url(self, expected_url):
        """
        Waits for the browser's current URL to match the expected URL.

        Args:
            expected_url (str): The URL to wait for.
        """
        self.wait.until(EC.url_to_be(expected_url))

    def get_current_url(self):
        """
        Gets the current URL of the browser.

        Returns:
            str: The current URL.
        """
        return self.driver.current_url

    def click_shopping_cart_icon(self):
        """
        Clicks the shopping cart icon and returns an instance of the CartPage.
        This provides a fluent interface for navigating between pages.

        Returns:
            CartPage: An instance of the CartPage class.
        """
        from pages.cart_page import CartPage
        self.click_element(self.SHOPPING_CART_ICON)
        return CartPage(self.driver)

    def get_shopping_cart_badge_count(self):
        """
        Retrieves the number of items in the shopping cart from the badge icon.

        Returns:
            int: The number of items, or 0 if the badge is not present.
        """
        try:
            badge_element = self.find_element(self.SHOPPING_CART_BADGE)
            return int(badge_element.text)
        except:
            return 0

    def select_by_value(self, locator, value):
        """
        Selects an option from a dropdown element by its value attribute.

        Args:
            locator (tuple): The locator for the dropdown element.
            value (str): The value of the option to select.
        """
        select_element = self.find_element(locator)
        select = Select(select_element)
        select.select_by_value(value)

    def click_burger_menu(self):
        """
        Clicks the burger menu icon and waits for the menu to appear.
        """
        self.click_element(self.BURGER_MENU_ICON)
        self.wait_for_element_is_displayed(self.BURGER_MENU_WRAPPER)

    def click_burger_logout(self):
        """
        Clicks the 'Logout' link in the burger menu and returns an instance of the LoginPage.

        Returns:
            LoginPage: An instance of the LoginPage class.
        """
        from pages.login_page import LoginPage
        self.click_element(self.BURGER_LOGOUT)
        return LoginPage(self.driver)

    def click_burger_menu_reset(self):
        """
        Clicks the 'Reset App State' link and closes the burger menu.
        This is a utility method for resetting the test environment.
        """
        self.click_element(self.BURGER_MENU_RESET)
        self.click_element(self.BURGER_MENU_CLOSE)

    def wait_for_element_is_displayed(self, locator):
        """
        Waits for an element to become visible on the page.

        Args:
            locator (tuple): The locator for the element.

        Returns:
            WebElement: The found web element.
        """
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
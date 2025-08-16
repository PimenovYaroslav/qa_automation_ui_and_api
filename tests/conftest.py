import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
import random
from endpoints.pet_api import PetAPI
from endpoints.user_api import UserAPI
from pages.cart_page import CartPage
from pages.checkout_page_1 import CheckoutPageOne
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from selenium.webdriver.chrome.options import Options
import allure

# Load environment variables from a .env file
load_dotenv()


@pytest.fixture(scope="session")
def config():
    """
    Provides configuration data loaded from environment variables.
    This fixture has a 'session' scope, meaning it's created once per test session.
    """
    return {
        "API": {
            "BASE_URL": os.getenv("API_BASE_URL"),
            "SPECIAL_KEY": os.getenv("API_SPECIAL_KEY")
        },
        "UI_SAUCEDEMO": {
            "BASE_URL": os.getenv("SAUCE_BASE_URL"),
            "USERNAME": os.getenv("SAUCE_USERNAME"),
            "PASSWORD": os.getenv("SAUCE_PASSWORD"),
            "LOCKED_USER": os.getenv("SAUCE_LOCKED_USER"),
            "PROBLEM_USER": os.getenv("SAUCE_PROBLEM_USER"),
            "PERFORMANCE_GLITCH_USER": os.getenv("SAUCE_PERFORMANCE_GLITCH_USER"),
            "ERROR_USER": os.getenv("SAUCE_ERROR_USER"),
            "VISUAL_USER": os.getenv("SAUCE_VISUAL_USER"),
            "INVALID_PASSWORD": os.getenv("SAUCE_INVALID_PASSWORD"),
        }
    }


@pytest.fixture(scope="function")
def driver(config, tmp_path):
    """
    Initializes and configures the Selenium WebDriver for Chrome.
    It uses a new, unique temporary directory for each test function to prevent
    'SessionNotCreatedException' errors.
    """
    base_url = config['UI_SAUCEDEMO']['BASE_URL']
    chrome_options = Options()

    # Create a unique temporary directory for the user data to prevent conflicts
    user_data_dir = os.path.join(tmp_path, "chrome-test-profile")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    # Add other configuration options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-password-manager-reauthentication")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "profile.default_content_setting_values.popups": 0,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize driver to None to prevent 'referenced before assignment' error
    driver = None
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(base_url)

        # Clear all cookies and storage to ensure a clean state
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")

        yield driver

    finally:
        # Check if the driver was successfully initialized before quitting
        if driver is not None:
            driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture a screenshot on test failure for Allure reports.
    This function is executed after each test function runs.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Check if the test failed during the 'call' phase
    if report.when == "call" and report.failed:
        try:
            # Get the driver instance from the test item
            driver = item.funcargs['driver']
            # Attach the screenshot to the Allure report
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Could not take a screenshot due to an error: {e}")


@pytest.fixture(scope="function")
def logged_in_standard_user(driver, config, login_page, products_page):
    """
    Logs in a standard user and navigates to the products page.
    This is a convenience fixture for tests that require an authenticated user state.
    Returns an instance of the ProductsPage.
    """
    login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
    login_page.login(config['UI_SAUCEDEMO']['USERNAME'], config['UI_SAUCEDEMO']['PASSWORD'])
    login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
    return products_page


# =========================================================================
# Page Object Fixtures
# These fixtures provide instances of page object classes to the tests,
# abstracting away the driver and making tests cleaner.
# =========================================================================

@pytest.fixture(scope="function")
def login_page(driver):
    """Provides an instance of the LoginPage."""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def products_page(driver):
    """Provides an instance of the ProductsPage."""
    return ProductsPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver):
    """Provides an instance of the CartPage."""
    return CartPage(driver)


@pytest.fixture(scope="function")
def checkout_page_1(driver):
    """Provides an instance of the CheckoutPageOne."""
    return CheckoutPageOne(driver)


# =========================================================================
# API Fixtures
# These fixtures set up API clients and test data for API tests.
# =========================================================================

@pytest.fixture(scope="session")
def pet_api_client(config):
    """
    Provides an API client for the Pet endpoint.
    'session' scope means the client is created once for the entire test session.
    """
    base_url = config['API']['BASE_URL']
    return PetAPI(base_url)


@pytest.fixture(scope="session")
def user_api_client(config):
    """
    Provides an API client for the User endpoint.
    'session' scope means the client is created once for the entire test session.
    """
    base_url = config['API']['BASE_URL']
    return UserAPI(base_url)


@pytest.fixture(scope="function")
def created_pet_id(pet_api_client):
    """
    Creates a new pet via API before a test and deletes it after the test.
    This ensures each test runs with a new, known pet entity.
    Yields the ID of the created pet.
    """
    # --- Setup: Create a pet ---
    pet_id = random.randint(1000000, 9999999)
    pet_name = f"TestPet_{pet_id}"
    pet_status = "available"
    pet_data = {
        "id": pet_id,
        "name": pet_name,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 200, "Failed to create pet"

    yield pet_id  # Provide the pet ID to the test

    # --- Teardown: Delete the pet ---
    pet_api_client.delete_pet(pet_id)


@pytest.fixture(scope="function")
def created_username(user_api_client):
    """
    Creates a new user via API before a test and deletes it after the test.
    This ensures test isolation by providing a fresh user for each test function.
    Yields the username of the created user.
    """
    # --- Setup: Create a user ---
    user_id = random.randint(1000000, 9999999)
    user_data = {
        "id": user_id,
        "username": f"Test_Name_{user_id}",
        "firstName": f"Test_First_{user_id}",
        "lastName": f"Test_Second_{user_id}",
        "email": f"mail_{user_id}@test.com",
        "password": str(user_id),  # Ensure password is a string
        "phone": f"093{user_id}",
        "userStatus": 0
    }
    create_user_response = user_api_client.create_user(user_data)
    assert create_user_response.status_code == 200, "Failed to create user"

    yield user_data["username"]  # Provide the username to the test

    # --- Teardown: Delete the user ---
    user_api_client.delete_user(user_data["username"])
class TestLoginPage:
    """
    Test suite for the SauceDemo login page.

    This class contains tests that verify login functionality for different user types,
    as well as handling invalid login attempts.
    """

    def test_successful_login_with_standard_user(self, driver, config, login_page, products_page):
        """
        Tests successful login with a standard user.

        Steps:
        1. Open the SauceDemo login page.
        2. Log in with a valid standard username and password.
        3. Wait for the products page to load.
        4. Assert that the current URL is the expected products page URL.
        5. Assert that the products page title is displayed.
        6. Assert that the products page title text is correct.
        """
        # Step 1: Navigate to the base URL
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        # Step 2: Perform the login action
        login_page.login(config['UI_SAUCEDEMO']['USERNAME'], config['UI_SAUCEDEMO']['PASSWORD'])
        # Step 3: Wait for the URL to change, confirming navigation
        login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
        expected_url = "https://www.saucedemo.com/inventory.html"
        # Step 4: Verify the browser is on the correct page
        assert products_page.get_current_url() == expected_url, \
            f"Expected URL to be {expected_url}, but got {products_page.get_current_url()}"
        # Step 5 & 6: Verify key elements on the products page are displayed and have the correct text
        assert products_page.is_products_page_displayed(), "Products page title is not displayed."
        assert products_page.get_products_title_text() == "Products", \
            f"Expected title 'Products', but got '{products_page.get_products_title_text()}'"

    def test_login_with_locked_user(self, driver, config, login_page):
        """
        Tests login with a locked-out user.

        Steps:
        1. Open the SauceDemo login page.
        2. Attempt to log in with a locked username and a valid password.
        3. Assert that the URL remains the login page.
        4. Assert that the correct "locked out" error message is displayed.
        """
        # Step 1: Navigate to the base URL
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        # Step 2: Attempt login with locked credentials
        login_page.login(config['UI_SAUCEDEMO']['LOCKED_USER'], config['UI_SAUCEDEMO']['PASSWORD'])
        expected_url = "https://www.saucedemo.com/"
        # Step 3: Verify the URL hasn't changed
        assert login_page.get_current_url() == expected_url, \
            f"Expected URL to remain {expected_url}, but got {login_page.get_current_url()}"
        # Step 4: Verify the specific error message is present
        assert login_page.get_error_message().lower() == "epic sadface: sorry, this user has been locked out.", \
            f"Expected 'locked out' error, but got '{login_page.get_error_message()}'"

    def test_login_with_problem_user(self, driver, config, login_page, products_page):
        """
        Tests login with a "problem" user, who encounters visual issues.
        This test confirms that the login itself is successful despite the UI problems.
        """
        # Step 1: Navigate to the base URL
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        # Step 2: Log in with a "problem" username and valid password
        login_page.login(config['UI_SAUCEDEMO']['PROBLEM_USER'], config['UI_SAUCEDEMO']['PASSWORD'])
        # Step 3: Wait for the products page to load
        login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
        expected_url = "https://www.saucedemo.com/inventory.html"
        # Step 4-6: Assert that navigation to the products page is successful
        assert products_page.get_current_url() == expected_url, \
            f"Expected URL to be {expected_url}, but got {products_page.get_current_url()}"
        assert products_page.is_products_page_displayed(), "Products page title is not displayed."
        assert products_page.get_products_title_text() == "Products", \
            f"Expected title 'Products', but got '{products_page.get_products_title_text()}'"

    def test_performance_glitch_user(self, driver, config, login_page, products_page):
        """
        Tests login with a "performance glitch" user, who experiences a delay.
        This test confirms the login is successful despite the performance issue.
        """
        # Step 1: Navigate to the base URL
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        # Step 2: Log in with a "performance glitch" username and valid password
        login_page.login(config['UI_SAUCEDEMO']['PERFORMANCE_GLITCH_USER'], config['UI_SAUCEDEMO']['PASSWORD'])
        # Step 3: Wait for the products page to load (this will handle the delay)
        login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
        expected_url = "https://www.saucedemo.com/inventory.html"
        # Step 4-6: Assert that navigation to the products page is successful
        assert products_page.get_current_url() == expected_url, \
            f"Expected URL to be {expected_url}, but got {products_page.get_current_url()}"
        assert products_page.is_products_page_displayed(), "Products page title is not displayed."
        assert products_page.get_products_title_text() == "Products", \
            f"Expected title 'Products', but got '{products_page.get_products_title_text()}'"

    def test_login_with_invalid_password(self, driver, config, login_page):
        """
        Tests login with a valid username but an invalid password.
        """
        # Step 1: Navigate to the base URL
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        # Step 2: Attempt login with a valid username and invalid password
        login_page.login(config['UI_SAUCEDEMO']['USERNAME'], config['UI_SAUCEDEMO']['INVALID_PASSWORD'])
        expected_url = "https://www.saucedemo.com/"
        # Step 3: Verify the URL hasn't changed
        assert login_page.get_current_url() == expected_url, \
            f"Expected URL to remain {expected_url}, but got {login_page.get_current_url()}"
        # Step 4: Verify the specific error message for invalid credentials is displayed
        expected_error_message = "Epic sadface: Username and password do not match any user in this service"
        actual_error_message = login_page.get_error_message()
        assert actual_error_message.lower() == expected_error_message.lower(), \
            f"Expected error message '{expected_error_message}', but got '{actual_error_message}'"

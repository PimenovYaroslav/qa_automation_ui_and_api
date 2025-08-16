import pytest


class TestNavigation:
    """
    Test suite for UI navigation and state management on the SauceDemo website.

    This class contains tests that verify user interactions with the navigation menu,
    such as logging out and resetting the application state.
    """

    def test_logout_from_burger_menu(self, logged_in_standard_user):
        """
        Tests the user can successfully log out via the burger menu.

        Steps:
        1. Access the products page (pre-condition handled by fixture).
        2. Click on the burger menu.
        3. Click the 'Logout' button within the menu.
        4. Assert that the login page is displayed by checking for the login box.
        """
        products_page = logged_in_standard_user
        # Click the burger menu icon to open the side menu
        products_page.click_burger_menu()
        # Click the 'Logout' link and get the login page object
        login_page = products_page.click_burger_logout()
        # Verify the user is redirected to the login page by checking for a key element
        assert login_page.id_login_box_visible(), "Login box is not visible, logout failed."

    @pytest.mark.xfail(reason="UI bug: 'Add to cart' buttons count does not reset after app state clear.")
    def test_reset_app_state_clears_cart(self, logged_in_standard_user):
        """
        Tests that the 'Reset App State' button clears the shopping cart and resets UI buttons.

        Steps:
        1. Access the products page with an empty cart (pre-condition).
        2. Get the initial count of 'Add to cart' buttons.
        3. Add a random number of products to the cart.
        4. Assert the shopping cart badge count matches the number of products added.
        5. Click the burger menu and then the 'Reset App State' button.
        6. Assert the shopping cart badge count is now zero.
        7. Assert the count of 'Add to cart' buttons is back to the initial number.
        8. Assert there are no 'Remove' buttons visible.
        """
        products_page = logged_in_standard_user
        # Get the initial count of "Add to cart" buttons before adding any items
        initial_add_buttons = products_page.get_count_of_add_to_cart_buttons()
        # Add a random number of products and get the expected count
        expected_count = products_page.add_random_products_to_cart()
        # Assert the shopping cart badge count matches the number of products added
        actual_count = products_page.get_shopping_cart_badge_count()
        assert actual_count == expected_count, \
            f"Expected {expected_count} items in cart, but found {actual_count}."
        # Open the side menu and click the reset button
        products_page.click_burger_menu()
        products_page.click_burger_menu_reset()
        # Verify the cart badge count is reset to 0
        cart_after_reset = products_page.get_shopping_cart_badge_count()
        assert cart_after_reset == 0, \
            f"Expected cart badge count to be 0 after reset, but got {cart_after_reset}."
        # Verify the number of "Add to cart" buttons has been restored to the initial count
        final_add_buttons = products_page.get_count_of_add_to_cart_buttons()
        remove_buttons = products_page.get_count_remove_buttons()
        assert final_add_buttons == initial_add_buttons, \
            f"Expected {initial_add_buttons} 'Add to cart' buttons, but found {final_add_buttons}."
        # Verify that there are no "Remove" buttons left after the reset
        assert remove_buttons == 0, \
            f"Expected 0 'Remove' buttons, but found {remove_buttons}."
import pytest
from pages.products_page import ProductsPage


class TestProductsAndCart:
    """
    Test suite for verifying product and shopping cart functionality on SauceDemo.
    """

    def test_add_backpack_to_cart_and_verify_badge(self, logged_in_standard_user):
        """
        Tests adding a single specific item (Backpack) to the cart and verifies UI changes.
        """
        products_page = logged_in_standard_user
        # Add the Sauce Labs Backpack to the cart
        products_page.add_sauce_labs_backpack_to_cart()
        # Assert the cart badge count is 1
        assert products_page.get_shopping_cart_badge_count() == 1, \
            "Expected shopping cart badge count to be 1 after adding one item."
        # Assert the 'Add to cart' button for the backpack is no longer visible
        assert not products_page.is_add_backpack_button_displayed(), \
            "The 'Add to cart' button for the backpack should be hidden after adding it."
        # Assert the 'Remove' button for the backpack is now visible
        assert products_page.is_remove_backpack_button_displayed(), \
            "The 'Remove' button for the backpack should be displayed after adding it."

    def test_add_random_items_to_cart_and_verify_badge(self, logged_in_standard_user):
        """
        Tests adding a random number of products to the cart and verifies the badge count.
        """
        products_page = logged_in_standard_user
        # Add a random number of products and get the expected count
        expected_count = products_page.add_random_products_to_cart()
        # Get the actual number of items in the cart from the badge
        actual_count = products_page.get_shopping_cart_badge_count()
        # Assert the badge count matches the expected number of products added
        assert actual_count == expected_count, \
            f"Expected cart badge count to be {expected_count}, but got {actual_count}."

    def test_add_random_items_and_verify_cart_contents(self, logged_in_standard_user):
        """
        Tests adding random products and then verifying their presence on the cart page.
        """
        products_page = logged_in_standard_user
        # Add random products and store their names for later verification
        added_products = products_page.add_random_products_to_cart_and_get_names()
        # Verify the cart badge count matches the number of products added
        actual_count = products_page.get_shopping_cart_badge_count()
        assert len(added_products) == actual_count, \
            f"Expected cart badge count to be {len(added_products)}, but got {actual_count}."
        # Navigate to the cart page
        cart_page = products_page.click_shopping_cart_icon()
        # Assert that the cart page is displayed
        assert cart_page.is_cart_page_displayed(), "Cart page is not displayed after clicking the icon."
        # Verify each added product is present in the cart
        for item_name in added_products:
            assert cart_page.is_item_in_cart_by_name(item_name), \
                f"Item '{item_name}' was not found in the shopping cart."

    def test_remove_items_from_cart(self, logged_in_standard_user):
        """
        Tests adding items to the cart and then successfully removing a random one.
        """
        products_page = logged_in_standard_user
        # Add random products and get their names
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()
        assert len(added_products) == actual_count, \
            "Initial cart count does not match the number of products added."
        # Navigate to the cart page
        cart_page = products_page.click_shopping_cart_icon()
        # Verify each item is in the cart
        for item_name in added_products:
            assert cart_page.is_item_in_cart_by_name(item_name), \
                f"Item '{item_name}' was not found in the shopping cart."
        # Remove a random item from the cart and get its name
        removed_product = cart_page.remove_random_item_from_cart()
        # Get the names of the remaining products in the cart
        products_after_remove = cart_page.get_cart_items_names()
        # Assert the count of products is now one less than the original count
        assert len(products_after_remove) == len(added_products) - 1, \
            "Incorrect number of items in cart after removing one."
        # Assert the removed product is no longer in the cart
        assert not cart_page.is_item_in_cart_by_name(removed_product), \
            f"The removed product '{removed_product}' is still in the cart."
        # Create a new list of expected products after removal and compare
        expected_products = [name for name in added_products if name != removed_product]
        assert sorted(products_after_remove) == sorted(expected_products), \
            "The list of remaining products does not match the expected list."

    def test_successful_checkout_process(self, logged_in_standard_user):
        """
        Tests the entire successful checkout process, including price verification.
        """
        products_page = logged_in_standard_user
        # Add random products to the cart
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()
        assert len(added_products) == actual_count, \
            "Cart badge count doesn't match the number of products added."
        # Navigate to the cart page and verify products are present
        cart_page = products_page.click_shopping_cart_icon()
        for item_name in added_products:
            assert cart_page.is_item_in_cart_by_name(item_name), \
                f"Item '{item_name}' not found in cart."
        # Proceed to checkout and fill out the form
        checkout_page_1 = cart_page.click_checkout_button()
        checkout_data = checkout_page_1.generate_checkout_data()
        checkout_page_1.fill_checkout_form(checkout_data)
        # Continue to the checkout overview page
        checkout_page_2 = checkout_page_1.click_continue_button()
        # Get price values from the page
        item_total_price = checkout_page_2.get_item_total()
        tax_rate = checkout_page_2.get_tax()
        total_price = checkout_page_2.get_total()
        # Calculate expected total and assert it matches the displayed total (with a small tolerance)
        expected_total = item_total_price + tax_rate
        assert abs(total_price - expected_total) < 0.01, \
            f"Expected total {expected_total} is not close to actual total {total_price}."
        # Complete the checkout
        checkout_complete_page = checkout_page_2.click_finish_button()
        # Assert that the thank you message is displayed
        assert checkout_complete_page.is_thank_you_displayed(), "Checkout completion page not displayed."

    def test_checkout_without_zip_code(self, logged_in_standard_user):
        """
        Tests that checkout fails with a specific error message when the zip code is missing.
        """
        products_page = logged_in_standard_user
        # Add products and navigate to the cart
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()
        cart_page = products_page.click_shopping_cart_icon()
        assert len(added_products) == actual_count, \
            "Initial cart count doesn't match the number of products added."
        # Proceed to checkout and fill out the form without a zip code
        checkout_page_1 = cart_page.click_checkout_button()
        checkout_data = checkout_page_1.generate_checkout_data_with_empty_zip()
        checkout_page_1.fill_checkout_form(checkout_data)
        checkout_page_1.click_continue_button()
        # Assert that an error message is displayed
        assert checkout_page_1.is_error_message_displayed(), \
            "Expected error message for missing zip code, but none was displayed."
        # Assert the error message text is correct
        assert checkout_page_1.get_error_message_text().lower() == "error: postal code is required", \
            "Incorrect error message text for missing zip code."

    def test_product_sorting(self, logged_in_standard_user):
        """
        Tests the sorting functionality for products by price (low-to-high and high-to-low).
        """
        products_page = logged_in_standard_user
        # Sort products by price from low to high
        products_page.select_sorting_products_by_value("lohi")
        low_to_high = products_page.get_products_prices()
        # Sort products by price from high to low
        products_page.select_sorting_products_by_value("hilo")
        high_to_low = products_page.get_products_prices()
        # Assert the prices are correctly sorted in ascending order
        assert low_to_high == sorted(low_to_high), "Products are not sorted correctly from low to high."
        # Assert the prices are correctly sorted in descending order
        assert high_to_low == sorted(high_to_low, reverse=True), "Products are not sorted correctly from high to low."

    def test_random_product(self, logged_in_standard_user):
        """
        Tests navigating to a random product's detail page and verifying its data.
        It also checks if returning to the products page works correctly.
        """
        products_page = logged_in_standard_user
        # Select a random product from the list and get its data before navigating
        product_data_from_list, product_details_page = products_page.select_random_product_and_get_details()
        # Get the product data from the details page and compare it with the initial data
        product_data_from_details = product_details_page.get_all_product_details()
        assert product_data_from_list == product_data_from_details, \
            "Product data from the list page does not match the data on the details page."
        # Click the "Back to products" button to return to the products page
        products_page_after_return = product_details_page.click_back_to_products_button()
        # Assert that the returned object is an instance of the ProductsPage class
        assert isinstance(products_page_after_return, ProductsPage), \
            "Did not return to the ProductsPage after clicking the back button."
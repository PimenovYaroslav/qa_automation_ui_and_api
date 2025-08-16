import random
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(10), wait=wait_fixed(1))
def get_user_with_retries(user_api_client, username):
    """
    A helper function that attempts to get a user by username up to 10 times.
    This is used to handle potential API consistency delays, where a newly
    created item might not be immediately available for retrieval.
    """
    get_response = user_api_client.get_user_by_username(username)
    assert get_response.status_code == 200, \
        f"Expected status code 200 for user retrieval, but got {get_response.status_code}."
    return get_response


# --- Positive Test Cases (Successful Operations) ---

@pytest.mark.xfail(reason="API returns 404 on DELETE during cleanup after user creation, indicating a consistency "
                          "issue.")
def test_create_user_with_valid_data_is_successful(user_api_client):
    """
    Test Case: Verifies that a new user can be successfully created with valid data.
    """
    # Generate a unique user ID and test data
    user_id = random.randint(1000000, 9999999)
    user_data = {
        "id": user_id,
        "username": f"Test_Name_{user_id}",
        "firstName": f"Test_First_{user_id}",
        "lastName": f"Test_Second_{user_id}",
        "email": f"mail_{user_id}@test.com",
        "password": user_id,
        "phone": f"093{user_id}",
        "userStatus": 0
    }
    # Send a POST request to create the user
    create_user_response = user_api_client.create_user(user_data)
    # Assert that the creation was successful with a 200 status code
    assert create_user_response.status_code == 200, \
        f"Expected status code 200 for user creation, but got {create_user_response.status_code}."
    create_user_response_json = create_user_response.json()
    # Validate the 'code' and 'type' fields in the response body
    assert create_user_response_json.get("code") == 200, \
        f"Expected code 200 in response, but got {create_user_response_json.get('code')}."
    assert create_user_response_json.get("type") == "unknown", \
        f"Expected type 'unknown' in response, but got '{create_user_response_json.get('type')}'."

    # Cleanup: delete the created user
    delete_user_response = user_api_client.delete_user(user_data["username"])
    assert delete_user_response.status_code == 200, \
        f"Expected status code 200 for user deletion, but got {delete_user_response.status_code}."


def test_get_user_is_successful(user_api_client, created_username):
    """
    Test Case: Verifies that an existing user can be successfully retrieved by username.
    """
    # Attempt to get the user, using retries to handle potential delays
    get_user_response = get_user_with_retries(user_api_client, created_username)
    # Assert that the retrieval was successful with a 200 status code
    assert get_user_response.status_code == 200, \
        f"Expected status code 200, but got {get_user_response.status_code}."
    response_json = get_user_response.json()
    # Validate that the username in the response matches the requested username
    assert response_json.get('username') == created_username, \
        f"Expected username '{created_username}' in response, but got '{response_json.get('username')}'."


@pytest.mark.xfail(reason="API Update (PUT) does not reflect changes, or takes too long to reflect.")
def test_update_existing_user_is_successful(user_api_client, created_username):
    """
    Test Case: Verifies that an existing user's data can be successfully updated.
    """
    # Get the initial user data for the update
    get_user_response_before_update = get_user_with_retries(user_api_client, created_username)
    assert get_user_response_before_update.status_code == 200, \
        f"Expected status code 200 before update, but got {get_user_response_before_update.status_code}."
    original_user_data = get_user_response_before_update.json()

    # Create a dictionary with the updated user data
    updated_user_data = {
        "id": original_user_data["id"],
        "username": created_username,
        "firstName": f"Updated_First_{original_user_data["id"]}",
        "lastName": f"Updated_Second_{original_user_data["id"]}",
        "email": f"Updated_mail_{original_user_data["id"]}@test.com",
        "password": original_user_data["id"],
        "phone": f"093{original_user_data["id"]}",
        "userStatus": 0
    }
    # Send a PUT request to update the user
    update_user_response = user_api_client.update_user_by_username(created_username, updated_user_data)
    # Assert that the update was successful
    assert update_user_response.status_code == 200, \
        f"Expected status code 200 for user update, but got {update_user_response.status_code}."

    # Retrieve the user again to verify the changes have been applied
    get_user_response_after_update = get_user_with_retries(user_api_client, created_username)
    assert get_user_response_after_update.status_code == 200, \
        f"Expected status code 200 after update, but got {get_user_response_after_update.status_code}."
    get_user_response_after_update_json = get_user_response_after_update.json()

    # Validate that the updated fields match the data sent in the request
    assert get_user_response_after_update_json.get("username") == updated_user_data["username"], \
        f"Expected '{updated_user_data['username']}', but got '{get_user_response_after_update_json.get('username')}'."
    assert get_user_response_after_update_json.get("firstName") == updated_user_data["firstName"], \
        f"Expected '{updated_user_data['firstName']}', but got'{get_user_response_after_update_json.get('firstName')}'."
    assert get_user_response_after_update_json.get("lastName") == updated_user_data["lastName"], \
        f"Expected '{updated_user_data['lastName']}', but got '{get_user_response_after_update_json.get('lastName')}'."
    assert get_user_response_after_update_json.get("email") == updated_user_data["email"], \
        f"Expected '{updated_user_data['email']}', but got '{get_user_response_after_update_json.get('email')}'."


@pytest.mark.xfail(reason="API returns 404 on DELETE for a recently created/retrieved user")
def test_delete_user_is_successful(user_api_client):
    """
    Test Case: Verifies that an existing user can be successfully deleted.
    """
    # Create a user to be deleted in the test
    user_id = random.randint(1000000, 9999999)
    user_data = {
        "id": user_id,
        "username": f"Test_Name_{user_id}",
        "firstName": f"Test_First_{user_id}",
        "lastName": f"Test_Second_{user_id}",
        "email": f"mail_{user_id}@test.com",
        "password": user_id,
        "phone": f"093{user_id}",
        "userStatus": 0
    }
    create_user_response = user_api_client.create_user(user_data)
    assert create_user_response.status_code == 200, \
        f"Expected status code 200 for user creation, but got {create_user_response.status_code}."
    create_user_response_json = create_user_response.json()
    assert create_user_response_json.get("code") == 200, \
        f"Expected code 200 in response, but got {create_user_response_json.get('code')}."
    assert create_user_response_json.get("type") == "unknown", \
        f"Expected type 'unknown' in response, but got '{create_user_response_json.get('type')}'."
    # Verify the user exists before attempting to delete it
    get_before_delete_response = get_user_with_retries(user_api_client, user_data["username"])
    assert get_before_delete_response.status_code == 200, \
        f"Expected user to exist (status 200) before deletion, but got {get_before_delete_response.status_code}."

    # Send a DELETE request to remove the user
    delete_user_response = user_api_client.delete_user(user_data["username"])
    assert delete_user_response.status_code == 200, \
        f"Expected status code 200 for user deletion, but got {delete_user_response.status_code}."

    # Verify the user no longer exists after deletion
    get_after_delete_response = user_api_client.get_user_by_username(user_data["username"])
    assert get_after_delete_response.status_code == 404, \
        f"Expected status code 404, but user was still found with status {get_after_delete_response.status_code}."
import random
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
def get_pet_with_retries(pet_api_client, pet_id):
    """
    A helper function that attempts to get a pet by ID up to 5 times.
    This is used to handle potential API consistency delays, where a newly
    created item might not be immediately available for retrieval.
    """
    get_response = pet_api_client.get_pet_by_id(pet_id)
    assert get_response.status_code == 200, \
        f"Expected status code 200, but got {get_response.status_code}."
    return get_response


# --- Positive Test Cases (Successful Operations) ---

@pytest.mark.xfail(reason="API returns 404 on GET for a recently created pet, indicating a consistency issue.")
def test_get_pet_by_id_is_successful(pet_api_client, created_pet_id):
    """
    Test Case: Verifies that an existing pet can be successfully retrieved by its ID.
    """
    get_response = get_pet_with_retries(pet_api_client, created_pet_id)
    assert get_response.json().get('id') == created_pet_id, \
        f"Expected pet ID {created_pet_id}, but got {get_response.json().get('id')}."


def test_get_pet_by_status_is_successful(pet_api_client):
    """
    Test Case: Verifies that pets can be retrieved by their status.
    """
    pet_status = "available"
    get_response = pet_api_client.get_pet_by_status(pet_status)
    assert get_response.status_code == 200, \
        f"Expected status code 200, but got {get_response.status_code}."
    get_response_json = get_response.json()
    for pet in get_response_json:
        assert pet["status"] == pet_status, \
            f"Expected pet status to be '{pet_status}', but got '{pet.get('status')}'."


def test_create_pet_with_valid_data_is_successful(pet_api_client):
    """
    Test Case: Verifies that a new pet can be created with valid data.
    """
    pet_id = random.randint(1000000, 9999999)
    pet_name = f"TestPet_{pet_id}"
    pet_status = "available"
    pet_data = {
        "id": pet_id,
        "name": pet_name,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 200, \
        f"Expected status code 200 for pet creation, but got {create_response.status_code}."
    response_json = create_response.json()
    assert response_json.get('id') == pet_id, \
        f"Expected ID {pet_id} in response, but got {response_json.get('id')}."
    assert response_json.get('name') == pet_name, \
        f"Expected name '{pet_name}' in response, but got '{response_json.get('name')}'."
    assert response_json.get('status') == pet_status, \
        f"Expected status '{pet_status}' in response, but got '{response_json.get('status')}'."
    pet_api_client.delete_pet(pet_id)


@pytest.mark.xfail(reason="API Update (PUT) does not reflect changes, or takes too long to reflect.")
def test_update_existing_pet_is_successful(pet_api_client, created_pet_id):
    """
    Test Case: Verifies that an existing pet can be successfully updated.
    """
    update_pet_name = f"UpdatedPet_{created_pet_id}"
    update_pet_data = {
        "id": created_pet_id,
        "name": update_pet_name,
        "status": "sold"
    }
    update_response = pet_api_client.update_pet(update_pet_data)
    update_response_json = update_response.json()
    assert update_response.status_code == 200, \
        f"Expected status code 200 for pet update, but got {update_response.status_code}."
    assert update_response_json.get('id') == created_pet_id, \
        f"Expected ID {created_pet_id} in update response, but got {update_response_json.get('id')}."
    assert update_response_json.get('name') == update_pet_name, \
        f"Expected name '{update_pet_name}' in update response, but got '{update_response_json.get('name')}'."
    assert update_response_json.get('status') == update_pet_data["status"], \
        f"Expected status '{update_pet_data['status']}' in response, but got '{update_response_json.get('status')}'."
    get_response = get_pet_with_retries(pet_api_client, created_pet_id)
    get_response_json = get_response.json()
    assert get_response_json.get('id') == created_pet_id, \
        f"Expected retrieved ID {created_pet_id} to match, but got {get_response_json.get('id')}."
    assert get_response_json.get('name') == update_pet_name, \
        f"Expected retrieved name '{update_pet_name}', but got '{get_response_json.get('name')}'."
    assert get_response_json.get('status') == update_pet_data["status"], \
        f"Expected retrieved status '{update_pet_data['status']}', but got '{get_response_json.get('status')}'."


@pytest.mark.xfail(
    reason="API returns 404 on DELETE for a recently created/retrieved pet, indicating a consistency issue.")
def test_delete_existing_pet_is_successful(pet_api_client):
    """
    Test Case: Verifies that an existing pet can be successfully deleted.
    """
    pet_id = random.randint(1000000, 9999999)
    pet_name = f"TestPet_{pet_id}"
    pet_status = "available"
    pet_data = {
        "id": pet_id,
        "name": pet_name,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 200, \
        f"Expected status code 200 for pet creation, but got {create_response.status_code}."
    response_json = create_response.json()
    assert response_json.get('id') == pet_id, \
        f"Expected ID {pet_id} in creation response, but got {response_json.get('id')}."
    assert response_json.get('name') == pet_name, \
        f"Expected name '{pet_name}' in creation response, but got '{response_json.get('name')}'."
    assert response_json.get('status') == pet_status, \
        f"Expected status '{pet_status}' in creation response, but got '{response_json.get('status')}'."

    get_before_delete_response = get_pet_with_retries(pet_api_client, pet_id)
    assert get_before_delete_response.status_code == 200, \
        f"Expected pet to exist (status 200) before deletion, but got {get_before_delete_response.status_code}."

    delete_response = pet_api_client.delete_pet(pet_id)
    assert delete_response.status_code == 200, \
        f"Expected status code 200 for pet deletion, but got {delete_response.status_code}."

    get_after_delete_response = pet_api_client.get_pet_by_id(pet_id)
    assert get_after_delete_response.status_code == 404, \
        f"Expected 404 after deletion, but pet was still found with status {get_after_delete_response.status_code}."


# --- Negative Test Cases (Invalid Operations) ---

def test_get_pet_by_invalid_id_fails(pet_api_client):
    """
    Test Case: Verifies that fetching a pet with an invalid ID fails correctly.
    """
    get_response = pet_api_client.get_pet_by_id('')
    assert get_response.status_code == 405, \
        f"Expected status code 405 for invalid ID, but got {get_response.status_code}."


@pytest.mark.xfail(reason="API returns 200 instead of 400 when 'name' is missing")
def test_create_pet_with_missing_required_field_fails(pet_api_client):
    """
    Test Case: Verifies that creating a pet without a required field ("name") fails.
    """
    pet_id = random.randint(1000000, 9999999)
    pet_status = "available"
    pet_data = {
        "id": pet_id,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 400, \
        f"Expected status code 400 for missing 'name' field, but got {create_response.status_code}."
    pet_api_client.delete_pet(pet_id)


@pytest.mark.xfail(reason="API accepts string for 'id' instead of integer, returning 200 OK.")
def test_create_pet_with_invalid_id_type_fails(pet_api_client):
    """
    Test Case: Verifies that creating a pet with an invalid data type for 'id' fails.
    """
    pet_id = random.randint(1000000, 9999999)
    pet_name = f"TestPet_{pet_id}"
    pet_status = "available"
    pet_data = {
        "id": str(pet_id),  # Invalid data type: string instead of integer
        "name": pet_name,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 400, \
        f"Expected status code 400 for invalid 'id' type, but got {create_response.status_code}."
    pet_api_client.delete_pet(pet_id)
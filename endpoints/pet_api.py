import os
import httpx


class PetAPI:
    """
    Client for interacting with the Pet Store API's /pet endpoint.
    This class encapsulates all HTTP requests related to pet management
    (create, read, update, delete).
    """

    def __init__(self, base_url=None):
        """
        Initializes the PetAPI client.

        Args:
            base_url (str, optional): The base URL of the Pet Store API.
                                      Defaults to "https://petstore.swagger.io/v2"
                                      if not provided.
        """
        # Set the base URL for API requests, defaulting if not provided
        self.base_url = base_url or "https://petstore.swagger.io/v2"
        # Construct the specific endpoint URL for pet operations
        self.pet_endpoint = f"{self.base_url}/pet"

    def create_pet(self, pet_data):
        """
        Sends a POST request to create a new pet in the store.

        Args:
            pet_data (dict): A dictionary containing the pet's data,
                             e.g., {"id": 1, "name": "doggie", "status": "available"}.

        Returns:
            httpx.Response: The response object from the API.
        """
        # Define the necessary headers for JSON content
        headers = {
            "Content-type": "application/json",  # Specifies that the request body is JSON
            "accept": "application/json"  # Indicates that the client expects a JSON response
        }
        # Send the POST request with the pet data as JSON
        response = httpx.post(self.pet_endpoint, json=pet_data, headers=headers)
        return response

    def update_pet(self, pet_data):
        """
        Sends a PUT request to update an existing pet's information.
        The pet is identified by its ID within the `pet_data`.

        Args:
            pet_data (dict): A dictionary containing the updated pet's data,
                             e.g., {"id": 1, "name": "updated_doggie", "status": "sold"}.

        Returns:
            httpx.Response: The response object from the API.
        """
        # Define the necessary headers for JSON content
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        # Send the PUT request with the updated pet data as JSON
        response = httpx.put(self.pet_endpoint, json=pet_data, headers=headers)
        return response

    def get_pet_by_id(self, pet_id):
        """
        Sends a GET request to retrieve a pet by its unique ID.

        Args:
            pet_id (int): The ID of the pet to retrieve.

        Returns:
            httpx.Response: The response object from the API.
        """
        # Construct the URL for fetching a specific pet by ID
        url = f"{self.pet_endpoint}/{pet_id}"
        # Send the GET request
        response = httpx.get(url)
        return response

    def get_pet_by_status(self, status):
        """
        Sends a GET request to find pets by their status.

        Args:
            status (str): The status of the pet(s) to find (e.g., "available", "pending", "sold").
                          Can be a comma-separated string for multiple statuses.

        Returns:
            httpx.Response: The response object from the API.
        """
        # Construct the URL for finding pets by status
        url = f"{self.pet_endpoint}/findByStatus"
        # Define headers, although often not strictly required for GET with params, good practice
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        # Define query parameters
        params = {"status": status}
        # Send the GET request with parameters
        response = httpx.get(url, params=params, headers=headers)
        return response

    def delete_pet(self, pet_id):
        """
        Sends a DELETE request to remove a pet from the store by its ID.
        Requires an API key for authentication.

        Args:
            pet_id (int): The ID of the pet to delete.

        Returns:
            httpx.Response: The response object from the API.

        Raises:
            ValueError: If the API key is not found in environment variables.
        """
        # Retrieve the API key from environment variables for authentication
        api_key = os.getenv("API_SPECIAL_KEY")
        # Ensure the API key is present
        if not api_key:
            raise ValueError("API key not found in environment variables!")

        # Construct the URL for deleting a specific pet by ID
        url = f"{self.pet_endpoint}/{pet_id}"
        # Define headers, including the API key for authorization
        headers = {
            "api_key": api_key
        }
        # Send the DELETE request with the API key
        response = httpx.delete(url, headers=headers)
        return response

import httpx


class UserAPI:
    """
    Client for interacting with the Pet Store API's /user endpoint.
    This class encapsulates all HTTP requests related to user management
    (create, read, update, delete).
    """

    def __init__(self, base_url=None):
        """
        Initializes the UserAPI client.

        Args:
            base_url (str, optional): The base URL of the Pet Store API.
                                      Defaults to "https://petstore.swagger.io/v2"
                                      if not provided.
        """
        # Set the base URL for API requests, defaulting to the Pet Store URL
        self.base_url = base_url or "https://petstore.swagger.io/v2"
        # Construct the specific endpoint URL for user operations
        self.user_endpoint = f"{self.base_url}/user"

    def create_user(self, user_data):
        """
        Sends a POST request to create a new user.

        Args:
            user_data (dict): A dictionary containing the user's data,
                              e.g., {"id": 1, "username": "johndoe", "email": "john@example.com"}.

        Returns:
            httpx.Response: The response object from the API.
        """
        # Define the necessary headers for JSON content
        headers = {
            "Content-type": "application/json",  # Specifies that the request body is JSON
            "accept": "application/json"         # Indicates that the client expects a JSON response
        }
        # Send the POST request with the user data as JSON
        response = httpx.post(self.user_endpoint, json=user_data, headers=headers)
        return response

    def update_user_by_username(self, username, updated_user_data):
        """
        Sends a PUT request to update an existing user by their username.

        Args:
            username (str): The username of the user to update.
            updated_user_data (dict): A dictionary with the updated user data.

        Returns:
            httpx.Response: The response object from the API.
        """
        # Define the necessary headers for JSON content
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        # Construct the URL for updating a specific user by username
        url = f"{self.user_endpoint}/{username}"
        # Send the PUT request with the updated user data as JSON
        response = httpx.put(url, json=updated_user_data, headers=headers)
        return response

    def get_user_by_username(self, username):
        """
        Sends a GET request to retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            httpx.Response: The response object from the API.
        """
        # Construct the URL for fetching a specific user by username
        url = f"{self.user_endpoint}/{username}"
        # Send the GET request
        response = httpx.get(url)
        return response

    def delete_user(self, username):
        """
        Sends a DELETE request to remove a user by their username.

        Args:
            username (str): The username of the user to delete.

        Returns:
            httpx.Response: The response object from the API.
        """
        # Construct the URL for deleting a specific user by username
        url = f"{self.user_endpoint}/{username}"
        # Send the DELETE request
        response = httpx.delete(url)
        return response

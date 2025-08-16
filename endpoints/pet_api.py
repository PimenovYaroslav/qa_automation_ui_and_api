import os
import httpx


class PetAPI:
    def __init__(self, base_url=None):
        self.base_url = base_url or "https://petstore.swagger.io/v2"
        self.pet_endpoint = f"{self.base_url}/pet"

    def create_pet(self, pet_data):
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        response = httpx.post(self.pet_endpoint, json=pet_data, headers=headers)
        return response

    def update_pet(self, pet_data):
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        response = httpx.put(self.pet_endpoint, json=pet_data, headers=headers)
        return response

    def get_pet_by_id(self, pet_id):
        url = f"{self.pet_endpoint}/{pet_id}"
        response = httpx.get(url)
        return response

    def get_pet_by_status(self, status):
        url = f"{self.pet_endpoint}/findByStatus"
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        params = {"status": status}
        response = httpx.get(url, params=params, headers=headers)
        return response

    def delete_pet(self, pet_id):
        api_key = os.getenv("API_SPECIAL_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables!")

        url = f"{self.pet_endpoint}/{pet_id}"
        headers = {
            "api_key": api_key
        }
        response = httpx.delete(url, headers=headers)
        return response

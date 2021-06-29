import requests
from constants import SheetyConst


class SheetyApi(SheetyConst):
    """Manages connection with sheety.co api"""
    def __init__(self):
        self.response_json = {}

    def add_data(self, data: dict, iata_code: str):
        """Adds row in google docs via sheety.co api"""
        record = {
            "price": {"city": data["city"],
                      "iataCode": iata_code,
                      "ticketsMaximumPrice": data["ticketsMaximumPrice"],
                      }
        }
        response = requests.post(url=self.SHEETY_ENDPOINT, headers=self.SHEETY_HEADERS, json=record)
        response.raise_for_status()

    def request_data(self):
        """Requests data from google doc sheet via sheety.co API"""
        response = requests.get(url=self.SHEETY_ENDPOINT, headers=self.SHEETY_HEADERS)
        response.raise_for_status()
        self.response_json = response.json()

    def update_data(self, price: str, row_id: int):
        """Updates row in google docs via sheety.co api"""
        record = {
            "price": {
                "ticketsMaximumPrice": price,
            }
        }
        url = self.SHEETY_ENDPOINT + f"/{row_id}"
        response = requests.put(url=url, headers=self.SHEETY_HEADERS, json=record)
        response.raise_for_status()

    def delete_data(self, row_id: int):
        """Deletes row in google docs via sheety.co api"""
        url = self.SHEETY_ENDPOINT + f"/{row_id}"
        response = requests.delete(url=url, headers=self.SHEETY_HEADERS)
        response.raise_for_status()

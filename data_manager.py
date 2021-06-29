from sheety_api import SheetyApi
from tequila_api import TequilaApi


class DataManager:
    """ Manages data from sheety.com and tequila apis"""
    def __init__(self):
        self.sheety_api = SheetyApi()
        self.tequila_api = TequilaApi()
        self.sheety_data = {}
        self.tequila_data = {}
        self.city_to_name = ""
        self.error_message = ""

    def request_data_from_sheety(self):
        """Fetches data from sheety.com api"""
        self.sheety_api.request_data()
        self.sheety_data = self.sheety_api.response_json

    def request_data_from_tequila(self, city: str):
        """Fetches data from tequila api"""
        self.tequila_api.request_data(city)
        self.tequila_data = self.tequila_api.response_json

    def does_city_exist(self, city):
        """Checks if the city exists in tequila api"""
        self.error_message = ""
        self.request_data_from_tequila(city)
        if not self.tequila_data["locations"]:
            self.error_message = "The city does not exist, please try different city name."
            return False
        else:
            return True

    def edit_data(self, data_to_update: dict):
        """ Adds or updates city (with corresponding IATA code) and price limit in google doc sheet
        via sheety.com API"""
        cities_in_data = [row["city"] for row in self.sheety_data["prices"]]
        if data_to_update["city"] in cities_in_data:
            row_id = cities_in_data.index(data_to_update['city']) + 2
            self.sheety_api.update_data(data_to_update["ticketsMaximumPrice"], row_id)
        else:
            if self.does_city_exist(data_to_update["city"]):
                iata_code = self.tequila_api.response_json["locations"][0]["code"]
                self.sheety_api.add_data(data_to_update, iata_code)

    def delete_city_row(self, city_to_delete: str):
        """Deletes row with city to be deleted in google doc via sheety.com api"""
        self.error_message = ""
        cities_in_data = [row["city"].lower() for row in self.sheety_data["prices"]]
        if city_to_delete.lower() in cities_in_data:
            row_to_delete = cities_in_data.index(city_to_delete.lower()) + 2
            self.sheety_api.delete_data(row_to_delete)
        else:
            self.error_message = "The city is not in the table."

    def is_found_city_the_same(self, city_to: str):
        """Checks if the city defined by the user is the same as fetched from tequila api"""
        self.tequila_api.request_data(city_to)
        try:
            self.city_to_name = self.tequila_api.response_json["locations"][0]["city"]["name"]
        except KeyError:
            self.city_to_name = self.tequila_api.response_json["locations"][0]["name"]
        finally:
            return city_to == self.city_to_name


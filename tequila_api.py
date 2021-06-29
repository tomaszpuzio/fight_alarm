import requests
from constants import TequilaConst


class TequilaApi(TequilaConst):
    """Manages connection with tequila api"""
    def __init__(self):
        self.response_json = {}

    def request_data(self, city):
        """Requests data from tequila API"""
        parameters = {
            "term": city,
        }
        response_tequila = requests.get(url=self.TEQUILA_QUERY_ENDPOINT, params=parameters,
                                        headers=self.TEQUILA_HEADERS)
        response_tequila.raise_for_status()
        self.response_json = response_tequila.json()

    def search_flights(self, fly_from: str, fly_to: str, date_from: str, date_to: str):
        """Requests data from tequila api"""
        parameters = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 21,
            "one_for_city": 1,
            "max_stopovers": 0,
        }
        response = requests.get(
            url=self.TEQUILA_SEARCH_ENDPOINT,
            params=parameters,
            headers=self.TEQUILA_HEADERS
        )
        response.raise_for_status()

        if not response.json()["data"]:
            parameters["max_stopovers"] = 2
            response = requests.get(
                url=self.TEQUILA_SEARCH_ENDPOINT,
                params=parameters,
                headers=self.TEQUILA_HEADERS)
            response.raise_for_status()

        self.response_json = response.json()

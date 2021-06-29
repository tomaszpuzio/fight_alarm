import datetime as dt


class FlightManager:
    """Manages the information about the flights"""
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.sheety_api = data_manager.sheety_api
        self.tequila_api = data_manager.tequila_api
        self.flight_available = []
        self.compressed_flight_data = {}
        self.hyperlinks = []
        self.stop_overs = 0
        self.via_city = ""
        self.error_message = ""

    def generate_flights_alarm_message(self, city_from: str):
        """Generates flight alarm message from the compressed flight data"""
        message = ""
        self.data_manager.request_data_from_sheety()
        city_to_codes = [row["iataCode"] for row in self.data_manager.sheety_data["prices"]]
        city_to_names = [row["city"] for row in self.data_manager.sheety_data["prices"]]

        for city_to_code in city_to_codes:
            city_to_id = city_to_codes.index(city_to_code)
            self.search_flight(city_from, city_to_code)
            flight_found = self.flight_available
            if not flight_found:
                message += f'No flights found for {city_from} to ' \
                           f'{city_to_names[city_to_id]}' \
                           f' trip meeting the criteria!\n\n'
            else:
                self.compress_flight_data(flight_found)
                if self.compressed_flight_data["price"] < \
                        self.data_manager.sheety_data["prices"][city_to_id]["ticketsMaximumPrice"]:
                    self.hyperlinks.append(self.compressed_flight_data["hyperlink"])
                    if self.stop_overs == 0:
                        message += f'Only {self.compressed_flight_data["price"]} Euro from ' \
                                   f'{self.compressed_flight_data["from_city"]} ' \
                                   f'to {self.compressed_flight_data["to_city"]}, from ' \
                                   f'{self.compressed_flight_data["from_date"]} ' \
                                   f'to {self.compressed_flight_data["to_date"]}\n\n'
                    else:
                        message += f'Only {self.compressed_flight_data["price"]} Euro from ' \
                                   f'{self.compressed_flight_data["from_city"]} ' \
                                   f'to {self.compressed_flight_data["to_city"]}, from ' \
                                   f'{self.compressed_flight_data["from_date"]} ' \
                                   f'to {self.compressed_flight_data["to_date"]}. Flight has' \
                                   f' {self.stop_overs}' \
                                   f' stop over via {self.via_city}\n\n'
                else:
                    message += f'No flights found for {self.compressed_flight_data["from_city"]} to ' \
                               f'{self.compressed_flight_data["to_city"]} trip meeting the criteria!\n\n'
        return message

    def search_flight(self, city_from: str, iata_to: str):
        """Sends request to tequila api to get data for the flight with departure city set by the user in
        Flight Alarm, and with arrival city read from google docs sheet"""
        self.tequila_api.request_data(city_from)
        iata_from = self.tequila_api.response_json["locations"][0]["code"]
        first_departure_date = dt.datetime.today() + dt.timedelta(days=1)
        first_departure_date_str = first_departure_date.strftime("%d/%m/%Y")
        last_departure_date = first_departure_date + dt.timedelta(weeks=24)
        last_departure_date_str = last_departure_date.strftime("%d/%m/%Y")

        self.tequila_api.search_flights(
            iata_from,
            iata_to,
            first_departure_date_str,
            last_departure_date_str,
        )
        self.flight_available = self.tequila_api.response_json["data"]

    def compress_flight_data(self, flight_data):
        """Compresses the flight data obtained with tequila api"""
        if flight_data:
            self.compressed_flight_data = {
                "price": flight_data[0]["price"],
                "from_city": flight_data[0]["cityFrom"] + "-" + flight_data[0]["flyFrom"],
                "to_city": flight_data[0]["cityTo"] + "-" + flight_data[0]["flyTo"],
                "from_date": flight_data[0]["route"][0]["local_departure"][:10],
                "to_date": flight_data[0]["route"][1]["local_departure"][:10],
                "hyperlink": [
                    f"{flight_data[0]['cityFrom']} - {flight_data[0]['cityTo']}",
                    f"{flight_data[0]['deep_link']}"
                ],
            }
            self.stop_overs = int(len(flight_data[0]["route"])/2 - 1)
            self.via_city = flight_data[0]["route"][0]["cityTo"]

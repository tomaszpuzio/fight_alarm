import os


class GuiConst:
    """Contains all the constants used within Fight Alarm app for GUI"""
    BG_COLOR = "#dff6f0"
    FG_COLOR = "#2e279d"
    BG_FONT = ("Courier", 35, "bold")
    FG_FONT = ("Courier", 12, "bold")
    FLIGHT_DISPLAY = "pictures/flights_display.png"
    BUTTON_COLOR = "#4d80e4"
    BUTTON_LETTERS_COLOR = "#ffffff"
    DELETE_BUTTON_COLOR = "#ec4646"
    BUTTON_FONT = ("Courier", 10, "bold")


class SheetyConst:
    """Contains all the constants used within Fight Alarm app for Sheety.io api"""
    SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
    SHEETY_AUTH = os.environ["SHEETY_AUTH"]
    SHEETY_HEADERS = {
        "Authorization": "Bearer " + SHEETY_AUTH
    }


class TequilaConst:
    """Contains all the constants used within Fight Alarm app for Tequila api"""
    TEQUILA_API_KEY = os.environ["TEQUILA_API_KEY"]
    TEQUILA_QUERY_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
    TEQUILA_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
    TEQUILA_HEADERS = {
        "apikey": TEQUILA_API_KEY
    }

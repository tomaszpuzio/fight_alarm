from tkinter import *
from tkinter import messagebox
from data_manager import DataManager
from flight_manager import FlightManager
from constants import GuiConst
from PIL import Image, ImageTk
import webbrowser


class MainWindow:
    """This is the GUI of the Flight alarm"""
    def __init__(self, master):
        self.master = master
        self.data_manager = DataManager()
        self.flight_manager = FlightManager(self.data_manager)

        self.master.resizable(width=False, height=False)
        self.master.title("Flight Alarm")
        self.master.config(padx=50, pady=20, bg=GuiConst.BG_COLOR)

        # ------------------------------- Images ------------------------------- #
        flight_display_img = Image.open(GuiConst.FLIGHT_DISPLAY)
        flight_display_img_resized = flight_display_img.resize((360, 255), Image.ANTIALIAS)
        self.flight_display_img = ImageTk.PhotoImage(flight_display_img_resized)

        # ------------------------------- Labels ------------------------------- #
        title_label = Label(
            master,
            text="Flight Alarm",
            bg=GuiConst.BG_COLOR,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.BG_FONT
        )
        title_label.grid(column=0, row=0, columnspan=3)

        flight_display_label = Label(
            master,
            image=self.flight_display_img
        )
        flight_display_label.grid(column=0, row=1, columnspan=2, pady=20, sticky="w")

        add_label = Label(
            master,
            text="Add/Update/Delete data",
            bg=GuiConst.BG_COLOR,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        add_label.grid(column=0, row=2, sticky="w", pady=5)

        city_to_label = Label(
            master,
            text="City to travel to: ",
            bg=GuiConst.BG_COLOR,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        city_to_label.grid(column=0, row=3, sticky="w")

        price_label = Label(
            master,
            text="Ticket's maximum price:",
            bg=GuiConst.BG_COLOR,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        price_label.grid(column=0, row=4, sticky="w")

        currency_label = Label(
            master,
            text="Euro",
            bg=GuiConst.BG_COLOR,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        currency_label.grid(column=1, row=4, sticky="e")

        city_from_label = Label(
            master,
            text="City to travel from: ",
            bg=GuiConst.BG_COLOR,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        city_from_label.grid(column=0, row=6, sticky="w", pady=5)

        # ------------------------------- Entries ------------------------------- #
        self.price_entry = Entry(
            master,
            width=7,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        self.price_entry.grid(column=1, row=4, sticky="w", pady=5)

        self.city_from_entry = Entry(
            master,
            width=12,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        self.city_from_entry.grid(column=1, row=6, sticky="w", pady=5)

        self.city_to_entry = Entry(
            master,
            width=12,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        self.city_to_entry.grid(column=1, row=3, sticky="w", pady=5)

        # ------------------------------- Buttons ------------------------------- #
        self.information_button = Button(
            master,
            text="Info",
            width=5,
            bg=GuiConst.BUTTON_COLOR,
            fg=GuiConst.BUTTON_LETTERS_COLOR,
            font=GuiConst.BUTTON_FONT,
            command=self.display_information_message
        )
        self.information_button.grid(column=2, row=0, sticky="e")

        self.add_update_button = Button(
            master,
            text="Add / Update",
            width=14,
            bg=GuiConst.BUTTON_COLOR,
            fg=GuiConst.BUTTON_LETTERS_COLOR,
            font=GuiConst.BUTTON_FONT,
            command=self.check_and_update_sheety_data_input
        )
        self.add_update_button.grid(column=1, row=5, sticky="w", pady=(5, 25))

        self.delete_button = Button(
            master,
            text="Delete data",
            width=14,
            bg=GuiConst.DELETE_BUTTON_COLOR,
            fg=GuiConst.BUTTON_LETTERS_COLOR,
            font=GuiConst.BUTTON_FONT,
            command=self.delete_sheety_data
        )
        self.delete_button.grid(column=0, row=5, sticky="w", pady=(5, 25))

        self.display_flight_alarm_message_button = Button(
            master,
            text="Check flights",
            width=14,
            bg=GuiConst.BUTTON_COLOR,
            fg=GuiConst.BUTTON_LETTERS_COLOR,
            font=GuiConst.BUTTON_FONT,
            command=self.display_flights_alarm_message
        )
        self.display_flight_alarm_message_button.grid(column=1, row=7, sticky="w")

        self.hyperlinks_button = Button(
            master,
            text="Hyperlinks",
            width=14,
            bg=GuiConst.BUTTON_COLOR,
            fg=GuiConst.BUTTON_LETTERS_COLOR,
            font=GuiConst.BUTTON_FONT,
            command=self.display_hyperlinks
        )
        self.hyperlinks_button.grid(column=2, row=7, sticky="e", pady=5)

        # ------------------------------- Text boxes ------------------------------- #
        self.cities_text_box = Text(
            master,
            height=14,
            width=40,
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        self.cities_text_box.grid(column=2, row=1, sticky="w", padx=(15, 0), pady=5)

        self.alarm_text_box = Text(
            master,
            height=10,
            width=40,
            wrap="word",
            fg=GuiConst.FG_COLOR,
            font=GuiConst.FG_FONT
        )
        self.alarm_text_box.insert(END, "Flight Alarm message...")
        self.alarm_text_box.config(state="disabled")
        self.alarm_text_box.grid(column=2, row=2, rowspan=5, sticky="w", padx=(15, 0), pady=5)

        self.display_sheety_data()

    def display_sheety_data(self):
        """Requests data from data manager and displays city and set maximum ticket's price in columns"""
        self.data_manager.request_data_from_sheety()
        self.cities_text_box.config(state="normal")
        self.cities_text_box.delete("1.0", END)
        cities_to_display = f"City | Maximum ticket's price (Euro) \n\n"
        for row in self.data_manager.sheety_data["prices"]:
            cities_to_display += f"{row['city']} | {row['ticketsMaximumPrice']} Euro\n"
        self.cities_text_box.insert(END, cities_to_display)
        self.cities_text_box.config(state="disabled")

    def check_and_update_sheety_data_input(self):
        """Updates the data in google docs via sheety.io api if no error occurred. In addition sends request to data
        manager to check if the city found by tequila api is same as put by the user. If it is not, the method
        displays a message to confirm the name of the city"""
        error_message = self.is_error_update_sheety_data()
        city_name = self.city_to_entry.get()
        if error_message:
            messagebox.showinfo(
                title="Input Info",
                message=error_message
            )
        elif not self.data_manager.does_city_exist(city_name):
            messagebox.showerror(
                title="City Error",
                message=self.data_manager.error_message
            )
        elif not self.data_manager.is_found_city_the_same(self.city_to_entry.get()) and not\
                self.data_manager.error_message:
            city_name = self.data_manager.city_to_name
            answer = messagebox.askquestion(
                title="Correct City",
                message=f"You typed {self.city_to_entry.get()}, however {city_name} was found in flight search. "
                        f"Is {city_name} the city you would like to fly to?"
            )
            if answer == "yes":
                self.update_sheety_data(city_name)
        else:
            self.update_sheety_data(city_name)

    def update_sheety_data(self, city):
        """Sends request to data manager to update the maximum price of the ticket for corresponding city"""
        update_data = {"city": city, "ticketsMaximumPrice": int(self.price_entry.get())}
        self.data_manager.edit_data(update_data)
        self.display_sheety_data()
        self.city_to_entry.delete(0, END)
        self.price_entry.delete(0, END)

    def delete_sheety_data(self):
        """Sends request to data manager to delete city from google doc via sheety.io api"""
        if self.is_error_delete_sheety_data():
            messagebox.showinfo(
                title="Input Info",
                message=self.is_error_delete_sheety_data()
            )
        else:
            city_to_delete = self.city_to_entry.get()
            self.data_manager.delete_city_row(city_to_delete)
            if self.data_manager.error_message:
                messagebox.showerror(
                    title="City Error",
                    message=self.data_manager.error_message
                )
            else:
                self.display_sheety_data()
                self.city_to_entry.delete(0, END)
                self.price_entry.delete(0, END)

    def display_flights_alarm_message(self):
        """Requests flight information (flight alarm message) from flight manager and
        displays the Flight Alarm message with all the cheapest flights found (or not)"""
        self.alarm_text_box.config(state="normal")
        self.alarm_text_box.delete("1.0", END)
        self.flight_manager.hyperlinks = []
        is_error, city_name = self.is_error_flights_alarm()
        if not is_error:
            flight_alarm = self.flight_manager.generate_flights_alarm_message(city_name)
            self.alarm_text_box.insert("1.0", flight_alarm)
        self.alarm_text_box.config(state="disabled")

    def is_error_delete_sheety_data(self):
        """Checks if the user properly filled the city to be deleted (if it is in the table and if it is of correct
        type"""
        error_message = ""
        if not self.city_to_entry.get():
            error_message = "Please fill in city name that you would like to delete. \n" \
                            "Note that the name has to be the same as in the table."
        elif not self.city_to_entry.get().replace(" ", "").isalpha():
            error_message = "Please note that city name should use only alphabetical characters."
        return error_message

    def is_error_update_sheety_data(self):
        """Checks if the user properly filled arrival city and maximum ticket's price (if both entries are filled
        and if both entries are of correct type"""
        error_message = ""
        if not self.city_to_entry.get() or not self.price_entry.get():
            error_message = "Please fill in both city name and ticket price to update or add data."

        elif not self.price_entry.get().replace(" ", "").isnumeric() or not \
                self.city_to_entry.get().replace(" ", "").isalpha():
            error_message = "Please note that city name should use only alphabetical characters," \
                            " while ticket price should be numeric."

        return error_message

    def is_error_flights_alarm(self):
        """Checks if the user properly filled departure city entry (if the entry is not empty, if the city exists,
        if the city typed is the same as found by tequila api)"""
        city_name = self.city_from_entry.get()
        if not city_name:
            messagebox.showinfo(
                title="Input Info",
                message="Please fill in city of departure."
            )
            return True, city_name
        elif not self.data_manager.does_city_exist(city_name):
            messagebox.showerror(
                title="City Error",
                message=self.data_manager.error_message
            )
            return True, city_name
        elif not self.data_manager.is_found_city_the_same(city_name) and not\
                self.data_manager.error_message:
            city_name = self.data_manager.city_to_name
            answer = messagebox.askquestion(
                title="Correct City",
                message=f"You typed {self.city_from_entry.get()}, however {city_name} was found in flight search. "
                        f"Is {city_name} the city you would like to fly from?"
            )
            if answer == "yes":
                return False, city_name
            else:
                return True, city_name
        else:
            return False, city_name

    def display_information_message(self):
        """Displays information about Flight Alarm in separate window"""
        self.alarm_text_box.config(state="normal")
        with open("READ_ME.txt") as file:
            message = file.read()
        messagebox.showinfo(title="Input Info",
                            message=message)
        self.alarm_text_box.config(state="disabled")

    def display_hyperlinks(self):
        """Displays hyperlinks in separate window"""
        hyperlinks_window = Toplevel(self.master)
        hyperlinks_window.title("Hyperlinks")
        hyperlinks_window.geometry("200x400")
        hyperlinks_window.config(
            padx=10,
            pady=10,
            bg=GuiConst.BG_COLOR
        )
        hyperlinks_window.resizable(width=False, height=False)

        background = Canvas(
            hyperlinks_window,
            width=165,
            height=370,
            bg="#ffffff",
        )
        background.pack(expand=True, fill=BOTH)

        if self.flight_manager.hyperlinks:
            for hyperlink in self.flight_manager.hyperlinks:
                flight_info_label = Label(
                    background,
                    text=hyperlink[0],
                    bg="#ffffff",
                    fg="#0000ff",
                    cursor="hand2"
                )
                flight_info_label.bind("<Button-1>", lambda e: self.open_browser(hyperlink[1]))
                flight_info_label.pack(pady=(10, 0), padx=10, fill=X)
        else:
            no_links_label = Label(
                background,
                text="No hyperlinks available.\n Check flights first.",
                bg="#ffffff",
                fg="#0000ff",
            )
            no_links_label.pack(pady=10, padx=10, fill=X)

    @staticmethod
    def open_browser(url):
        webbrowser.open_new(url)

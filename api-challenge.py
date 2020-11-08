"""Week 3 Coding Temple API Challenge Solution."""
import requests
import json
from pprint import pprint
from datetime import datetime


class Meeting_Schedule:
    def __init__(self):
        response = requests.get("https://ct-api-challenge.herokuapp.com/")
        self.partners = response.json()["partners"]
        self.meetings_dict = {}
        self.meetings_list = []

    def sort_by_country(self):
        """Make a seperate dictionary for each country."""
        for partner in self.partners:
            if not partner["country"] in self.meetings_dict:
                self.meetings_dict[partner["country"]] = {"possible_dates": {},
                                                          "name": partner["country"],
                                                          "available_partners": []}

            for date in partner["availableDates"]:
                if not date in self.meetings_dict[partner["country"]]["possible_dates"]:
                    self.meetings_dict[partner["country"]]["possible_dates"][date] = 1

                else:
                    self.meetings_dict[partner["country"]]["possible_dates"][date] += 1

    def choose_date(self):
        """Chose the best date for each country."""
        for country in self.meetings_dict:
            sorted_times_keys = sorted(self.meetings_dict[country]["possible_dates"].keys())

            ideal_dates = sorted_times_keys[0:2]
            max_attendees = (self.meetings_dict[country]["possible_dates"][sorted_times_keys[0]] +
                         self.meetings_dict[country]["possible_dates"][sorted_times_keys[1]])

            for i in range(1, len(sorted_times_keys)):
                date1 = datetime.strptime(sorted_times_keys[i], "%Y-%m-%d")
                date2 = datetime.strptime(sorted_times_keys[i - 1], "%Y-%m-%d")

                if (date1 - date2).days == 1:
                    current_attendees = (self.meetings_dict[country]["possible_dates"][sorted_times_keys[i]] +
                                         self.meetings_dict[country]["possible_dates"][sorted_times_keys[i - 1]])

                    if current_attendees > max_attendees:
                        max_attendees = (self.meetings_dict[country]["possible_dates"][sorted_times_keys[i]] +
                                         self.meetings_dict[country]["possible_dates"][sorted_times_keys[i - 1]])
                        ideal_dates = [sorted_times_keys[i], sorted_times_keys[i - 1]]

            self.meetings_dict[country]["possible_dates"] = ideal_dates
            self.meetings_dict[country]["start_date"] = ideal_dates[0]

    def add_attendees(self):
        """Add all partners that can attend each meeting."""
        for partner in self.partners:
            if (self.meetings_dict[partner["country"]]["possible_dates"][0] in partner["availableDates"] and 
                self.meetings_dict[partner["country"]]["possible_dates"][1] in partner["availableDates"]):
                self.meetings_dict[partner["country"]]["available_partners"].append(partner["email"])

    def update_meetings_list(self):
        """Push dictionary to the final meetings list."""
        for country in self.meetings_dict:
            self.meetings_dict[country]["attendees"] = len(self.meetings_dict[country]["available_partners"])
            del self.meetings_dict[country]["possible_dates"]
            self.meetings_list.append(self.meetings_dict[country])

    def organize_meetings_two(self):
        """Organize meetings for each country passed."""
        self.sort_by_country()
        self.choose_date()
        self.add_attendees()
        self.update_meetings_list()

        return self.meetings_list

schedule = Meeting_Schedule()
pprint(schedule.organize_meetings_two())
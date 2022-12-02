"""
This file contains the classes for the users choices of character
"""

import gspread
from google.oauth2.service_account import Credentials

import story_text as text
import story
from functions import GameFunctions as function

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Destiny_RPG_Multifile')

stats_worksheet = SHEET.worksheet('PlayerStats')


class Player:
    """
    Class for player inventory and weapon.
    """

    def __init__(self, items, health):
        self.items = items
        self.health = health


guardian = Player([], 100)


class UserInputs:
    """ Get player inputs for name, class and subclass """

    def get_name(self):
        """
        Get the name of the player.
        """
        function.s_print(self, text.CHOOSE_NAME_TEXT)

        while True:
            name = input("\n> ").capitalize()
            # https://www.w3schools.com/python/ref_string_isalpha.asp
            if not name.isalpha():
                print("Please enter letters only.")
            elif len(name.strip(" ")) < 3:
                print("Please enter a name at least 3 letters long.")
            else:
                function.s_print(self, f"It's nice to meet you, {name}."
                                 " I'm your Ghost.")
                self.get_class()
        return name

    def get_class(self):
        """
        Player chooses their class. 3 available based on Destiny lore.
        """
        function.s_print(self, text.CHOOSE_CLASS_TEXT)

        while True:
            chosen_class = input("My class is: \n> ").capitalize()
            classes = ["Hunter", "Warlock", "Titan"]
            if chosen_class in classes:
                function.s_print(self, f"Welcome, {chosen_class}.")
                print("\n")
                stats_worksheet.update_cell(2, 1, chosen_class)
                UserInputs.get_subclass(self, chosen_class)
            else:
                print("Please type either Hunter, Warlock or Titan.")
                continue

    def get_subclass(self, chosen_class):
        """Players choose their subclass - each class has 3."""

        function.s_print(self, text.CHOOSE_SUBCLASS_TEXT)

        if chosen_class == "Hunter":
            subclasses = ['Nightstalker', 'Blade Dancer', 'Gunslinger']

        elif chosen_class == "Warlock":
            subclasses = ['Voidwalker', 'Sunsinger', 'Stormcaller']

        elif chosen_class == "Titan":
            subclasses = ['Striker', 'Defender', 'Sunbreaker']

        for index, subclass in enumerate(subclasses, 1):
            print(index, subclass)

        while True:
            try:
                choice = int(input(f"\nMake your choice, {chosen_class}."
                                   "\n1, 2 or 3?\n>"))
                if choice < 1 or choice > 3 or choice == str():
                    raise ValueError("Please enter number 1, 2 or 3.")
            except ValueError:
                print("Please enter number 1, 2 or 3.")
            else:
                function.s_print(self, f"A {subclasses[choice-1]}?")
                function.s_print(self, "The darkness doesn't stand a chance\n")
                chosen_subclass = subclasses[choice-1]
                stats_worksheet.update_cell(2, 2, chosen_subclass)
                UserInputs.player_abilites(self, chosen_subclass)
                story.Story.opening_scene(self)

    def player_abilites(self, chosen_subclass):
        """
        Gives the player an ability, based on their choice of subclass
        """

        if chosen_subclass in ('Nightstalker', 'Voidwalker', 'Defender'):
            ability = 'Vortex Grenade'

        elif chosen_subclass in ("Blade Dancer", "Stormcaller", "Striker"):
            ability = 'Lightning Grenade'

        elif chosen_subclass in ("Gunslinger", "Sunsinger", "Sunbreaker"):
            ability = 'Solar Grenade'

        stats_worksheet.update_cell(2, 3, ability)
        return ability

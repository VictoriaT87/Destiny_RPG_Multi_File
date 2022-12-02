"""
This file contains the story scenes layed out.
It calls on the functions, text and character files.
"""

import sys
import random
import pyfiglet

import gspread
from google.oauth2.service_account import Credentials

from functions import GameFunctions as function
import story_text as text
import character


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


class Story:
    """
    Functions for the story and player choices
    """

    def introduction(self):
        """
        First function to run on Start.
        Logo image, introduction text, luck roll and worksheet cleared
        """

        text1 = pyfiglet.figlet_format("DESTINY", justify="center")
        text2 = pyfiglet.figlet_format("RPG GAME", justify="center")
        print(text1)
        print(text2)

        function.s_print(self, text.INTRODUCTION_TEXT)

        function.clear_worksheet(self)
        function.inital_luck(self)

        while True:
            start = input("Press the ENTER key to begin!\n")
            if start == "":
                function.reset_console(self)
                character.UserInputs.get_name(self)
            else:
                print(f"You typed '{start}'. When you're ready to"
                      " begin. press ENTER.")
                continue

    def opening_scene(self):
        """
        First scene to play after choosing a name and class
        """

        function.s_print(self, text.FIRST_SCENE_TEXT)

        while True:
            user_input = input("\n> ")
            if user_input == "1":
                self.search_cars()
            elif user_input == "2":
                self.building_entrance()
            elif user_input == "3":
                function.s_print(self, "You run towards the cliff and jump!"
                                 " This is all too much to take. [END]")
                function.clear_worksheet(self)
                sys.exit()
            else:
                print("Please enter number 1, 2 or 3.")
                continue

    def search_cars(self):
        """
        Function to search the cars
        """

        function.s_print(
            self, "You decide to search through some of the abandoned cars.")
        function.check_items(self)

        if character.guardian.items == ["key"]:
            function.s_print(self, "You put your key away and walk towards"
                             " the building.")
            self.building_entrance()
        else:
            function.s_print(self, "But you didn't find anything")
            self.building_entrance()

    def building_entrance(self):
        """
        Function to enter the building and try to open a chest
        """

        function.s_print(self, text.ENTRANCE_TEXT)
        function.open_chest(self)

    def building_hallway(self):
        """
        Function to play scene on entering the building hallway,
        call fight scene or end
        """
        function.s_print(self, text.HALLWAY_TEXT)

        while True:
            user_input = input("\n> ")
            if user_input == "1":
                function.s_print(self, "You enter door 1. It's a small room"
                                 " with a Fallen Dreg inside!")
                self.dreg_fight()
            if user_input == "2":
                function.s_print(
                    self, "You decide to enter the 2nd door."
                    " It's a small room.")
                self.empty_room()
            if user_input == "3":
                self.spaceship_room()
            else:
                print("Please enter number 1, 2 or 3.")
                continue

    def empty_room(self):
        """
        Empty room, player must turn around and choose another option
        from building_hallway
        """
        function.handle_vandal(self)

        function.s_print(self, text.EMPTY_ROOM_TEXT)

        while True:
            user_input = input("\n> ")
            if user_input == "1":
                function.s_print(self, "You enter door 1. It's a small room"
                                 " with a Fallen Dreg inside!")
                self.dreg_fight()
            if user_input == "2":
                self.spaceship_room()
            else:
                print("Please enter number 1 or 2.")
                continue

    def dreg_fight(self):
        """
        fight scene function, checks for weapon from random roll
        or else use abilities
        """
        player_class = stats_worksheet.cell(2, 1).value
        player_subclass = stats_worksheet.cell(2, 2).value
        player_ability = stats_worksheet.cell(2, 3).value
        stored_weapon = stats_worksheet.cell(2, 4).value

        # Health system from Elijah Henderson
        # https://www.youtube.com/watch?v=n17Hkgi8rt4
        character.guardian.health -= random.randint(1, 100)
        function.s_print(self, "\nBefore you can make a move, the Dreg"
                         " takes one shot with "
                         "his weapon.\nIt hits you on the arm!"
                         )
        print(f"\nHealth: {character.guardian.health}")
        if character.guardian.health < 0:
            function.s_print(
                self, "You are dead!\nWould you like to play again?")
            function.play_again(self)

        if stored_weapon is not None:
            function.s_print(self, "\nNow it's your turn!")
            function.s_print(self, f"You pull out your {stored_weapon}")
            function.s_print(
                self, "line up on the Dreg's head...\nand pull the trigger.")
            function.s_print(self, "Nice work!")
            self.hallway_choice()
        else:
            function.s_print(self, "\nNow it's your turn!")
            function.s_print(
                self, "You don't have a gun... but you do"
                " have your abilities\n")
            function.s_print(
                self, f"You're a {player_class}. A {player_subclass}.")
            function.s_print(self, f"You can use your {player_ability}")
            function.s_print(self, "You throw it and it sticks to the Dreg")
            function.s_print(self, "and explodes in a burst of Light!\n")
            function.s_print(self, "Nice work! The Dreg is dust.")
            self.hallway_choice()

    def hallway_choice(self):
        """
        User chooses between 2 paths
        """
        function.handle_vandal(self)

        function.s_print(self, "\nAhead, you see 2 corridors. ")
        function.s_print(self, "Do you want to go left, right or back?")

        while True:
            user_input = input("\n> ").capitalize()
            if user_input == "Left":
                function.s_print(
                    self, "You go left and ahead of you see a giant room")
                function.s_print(self, "with a spaceship. You check it out.")
                self.spaceship_room()
            elif user_input == "Right":
                function.s_print(self, "You go right. It's very hard to see.")
                function.s_print(
                    self, "In the darkness, you can make out something large")
                function.s_print(self, "with a glowing purple eye!")
                self.luck_escape()
            elif user_input == "Back":
                function.s_print(
                    self, "'I'm done fighting these Dregs, I'm out of here!"
                    "'[END]")
                function.clear_worksheet(self)
                sys.exit()
            else:
                print("Please enter either left, right or back.")
                continue

    def spaceship_room(self):
        """
        Spaceship room choice function
        """
        function.s_print(self, text.SPACESHIP_ROOM_TEXT)

        user_input = ""

        while True:
            luck = stats_worksheet.cell(2, 5).value

            user_input = input("\n> ").capitalize()
            if user_input == "Fight":
                if luck >= "50":
                    function.s_print(self, text.CAPTAIN_FIGHT_WIN_TEXT)
                    function.play_again(self)

                elif luck <= "49":
                    function.s_print(self, text.CAPTAIN_FIGHT_LOSE_TEXT)
                    function.play_again(self)

            elif user_input == "Run":
                function.s_print(self, text.CAPTAIN_FIGHT_RUN)
                function.play_again(self)
            else:
                print("Please enter either fight or run.")
                continue

    def luck_escape(self):
        """
        Function to check whether the player escapes from the ambush
        """
        if function.inital_luck(self) > 50:
            function.s_print(self, text.LUCK_ROLL_WIN)
            self.spaceship_room()
        else:
            function.s_print(self, text.LUCK_ROLL_LOSE)
            function.play_again(self)


def main():
    """Start the game"""

    new_story = Story()

    new_story.introduction()

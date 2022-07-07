from tinydb import TinyDB, where
from model.tournament import Tournament
#from model.player import Player

from tkinter import *
from tkinter import ttk


class TournamentController:

    def __init__(self, root):
        self.root = root
        self.tournament_name = ""

    def read_data(self):
        all_tournament_data = Tournament.read_data()
        tournament_instance_list = []
        players_list = []
        rounds_list = []
        for element in all_tournament_data:
            tournament_data = []
            for values in element.values():
                tournament_data.append(values)

            tournament_data.append(players_list)
            tournament_data.append(rounds_list)
            tournament = Tournament(tournament_data)
            tournament_instance_list.append(tournament)
        return tournament_instance_list

    def add_tournament_button_action(
            self, input_list, frame, y, add_tournament_button):
        data = list()
        data_check = True

        for element in input_list:
            # Get all input
            data.append(element.get())
            # Check if field is empty or not
            if not element.get():
                data_check = False

        if data_check:
            players_list = {}
            rounds_list = []
            data.append(players_list)
            data.append(rounds_list)

            tournament = Tournament(data)
            tournament.serialize_tournaments()
            tournament.write_data()

            self.refresh_tournament_frame()

    def display_player_window(self):
        from view.mainMenu import MainMenu  # Outside déclaration
        self.main_menu = MainMenu(self.root)
        self.main_menu.display_menu_window()

        from view.playerView import PlayerView      # Outside déclaration
        self.player_window = PlayerView(self.root)
        self.player_window.display_player_window()  # rattache a id
        self.player_window.player_data_set()

    def display_add_player_window(self, t):
        # Appelé depuis tournamentView: def tour_db_click(self)
        # tournament_selected = n° ligne, value = valeurs colonnes
        # print("val:", temp[0])  # Nom du tournoi

        # ========== Nouvelle fenêtre============================
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()
        # =======================================================
        tournament_name = t
        from view.playerView import PlayerView  # Outside déclaration
        self.player_window = PlayerView(self.root)
        self.player_window.call_tournament_player_list(tournament_name)
        self.player_window.player_data_set(tournament_name)

    def refresh_tournament_frame(self):
        """Clean root window and display menu"""
        from view.mainMenu import MainMenu
        main_menu = MainMenu(self.root)
        main_menu.display_tournament_window()

    def quit_tournament_window(self):
        self.t_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()
from model.player import Player
from tinydb import TinyDB
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tinydb import TinyDB, Query, where
from control.tournamentController import TournamentController
from datetime import datetime, timedelta


class PlayerController:

    def __init__(self, root):
        self.root = root
        self.start_date = None

    def add_player_tree_frame(self, input_list, frame, tree_frame,  y, tournament_name, add_player_button, data_fields):
        data = list()
        data.append(tournament_name)  # test TOURNOI
        data_check = True

        for element in input_list:
            data.append(element.get())
            if not element.get():
                data_check = False
        if data_check:
            data.append('0')  # score            
            player = Player(data)
            player.serialize_player()
            player.write_data()

        tree_frame.tag_configure('oddrow', background="white")
        tree_frame.tag_configure('evenrow', background="lightblue")
        count = len(tree_frame.get_children())
        if count % 2 == 0:
            tree_frame.insert('', 'end', text='', values=data, tags='evenrow')
        else:
            tree_frame.insert('', 'end', text='', values=data, tags='oddrow')
        count += 1        


    def delete_player_button_action(self, tree_frame):
        """Delete all players selected in database"""
        player_selected = tree_frame.focus()
        temp = tree_frame.item(player_selected,
                                    'values')  # tournament_selected = n° ligne, value = valeurs colonnes
        

        for element in tree_frame.selection():
            print("elt à détruire",element)
            tree_frame.delete(player_selected)
            Player.delete_player_data(temp[1])

    def delete_all_players_button_action(self, t):
        """Delete all players in tournaments_datas"""

        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        tournament_players_data = players_table.search(where('tournament_name') == t)
        print("delete_all_fct:", tournament_players_data)

        

    def refresh_player_frame(self,t):
        """Clean root window and display menu"""
        from view.mainMenu import MainMenu
        self.main_menu = MainMenu(self.root)

    def quit_player_window(self):
        # menu_controller = MenuController(self.root)
        # self.menu_controller.clean_window()
        self.p_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()

    def display_tournament_round_window(self, t):
        # ========== Nouvelle fenêtre============================
        from view.mainMenu import MainMenu   # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)

        from view.roundView import RoundView
        self.round_window = RoundView(self.root)
        self.round_window.display_round_window()

        self.start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.round_window.gen_round1(t)
        self.round_window.round_data_set(t, self.start_date)

        

    
		
       

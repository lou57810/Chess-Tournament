from tinydb import TinyDB, Query, where

import tkinter as tk
from tkinter import *
from tkinter import ttk

from control.tournamentController import TournamentController
from control.roundController import RoundController
from model.player import Player
from datetime import datetime, timedelta



class PlayerController:

    def __init__(self, root):
        self.root = root
        self.start_date = None

    def add_player_tree_frame(self, input_list, frame, tree_frame,  y, tournament_name, add_player_button, data_fields):
        data = list()
        data.append(tournament_name)
        data_check = True

        for element in input_list:
            data.append(element.get())
            if not element.get():
                data_check = False
        if data_check:
            data.append('0.0')  # score
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

    def modify_one_record(self, tree_frame, f_name_box, l_name_box, date_box, radiobutton1,
                                      radiobutton2, class_spin_box, tournament_name):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')

        selected = tree_frame.focus()
        value = tree_frame.item(selected, 'values')
        if radiobutton1.invoke == "Homme":
            gender_var = "Homme"
        else:
            gender_var = "Femme"
        # Updating treeview
        tree_frame.item(selected, text="", values=(
                        tournament_name,
                        f_name_box.get(),
                        l_name_box.get(),
                        date_box.get(),
                        gender_var,
                        class_spin_box.get(),
                        value[6]))

        name = f_name_box.get()
        players_table.update({'rank': class_spin_box.get()}, where('first_name') == name)  #where(('tournament_name' == tournament_name) & ('first_name' == name)))

    def select_one_record(self, tree_frame, f_name_box, l_name_box, date_box, radiobutton1,
                                      radiobutton2, class_spin_box):
        selected = tree_frame.focus()
        values = tree_frame.item(selected, 'values')

        f_name_box.delete(0,END)
        l_name_box.delete(0, END)
        date_box.delete(0, END)
        radiobutton1.deselect()
        radiobutton2.deselect()
        class_spin_box.delete(0, END)

        f_name_box.insert(0, values[1])
        l_name_box.insert(0, values[2])
        date_box.insert(0, values[3])
        if values[4] == "Homme":
            radiobutton1.invoke()
        else:
            radiobutton2.invoke()
        class_spin_box.insert(0, values[5])

    def delete_player_button_action(self, tree_frame):
        player_selected = tree_frame.focus()
        temp = tree_frame.item(player_selected, 'values')  # tournament_selected = n° ligne, value = valeurs colonnes

        for element in tree_frame.selection():
            tree_frame.delete(player_selected)
            Player.delete_player_data(temp[1])

    def delete_all_players_button_action(self, t):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        tournament_players_data = players_table.search(where('tournament_name') == t)

    def refresh_player_frame(self,t):
        from view.mainMenu import MainMenu
        self.main_menu = MainMenu(self.root)

    def quit_player_window(self):
        self.p_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()

    def display_tournament_round_window(self, tournament_name): # t -> tournament_name
        # ========== Nouvelle fenêtre============================
        from view.mainMenu import MainMenu   # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)

        from view.roundView import RoundView
        self.round_window = RoundView(self.root)
        self.round_window.display_round_window()

        self.start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.round_window.gen_rounds(tournament_name)
        self.round_window.round_data_set(tournament_name, self.start_date)

    def quitPlayerWindow(self):
        self.frame.destroy()



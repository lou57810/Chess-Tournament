from datetime import datetime
from model.player import Player
from tinydb import where, Query
from model.dbInterface import Interface
import tkinter as tk


class PlayerController:
    def __init__(self, root):
        self.root = root
        self.model_interface = Interface()
        self.start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def reg_tournament_player(self, tournament_name, input_list, count):
        data = list()
        data.append(tournament_name)
        data_check = True
        # count = len(tree_frame.get_children())

        for element in input_list:
            data.append(element.get())
            if not element.get():
                data_check = False
        if data_check:
            data.append('0.0')  # score
            data.append(count + 1)
            player = Player(data)
            player.serialize_player()
            player.write_data()
        return data

    def quit_player_window(self):
        self.p_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()

    def quitPlayerWindow(self):
        self.frame.destroy()

    def delete_all_players_button(self, tree_frame):
        tournament_name = tree_frame.item('I002', 'values')[0]

        for values in tree_frame.get_children():
            tree_frame.delete(values)

        players_table = self.model_interface.set_db_players_env()
        players_table.remove(where('tournament_name') == tournament_name)

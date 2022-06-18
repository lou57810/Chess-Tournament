from tinydb import TinyDB, Query, where
import tkinter as tk
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import ttk as tk

from model.round import Round
#from control.playerController import PlayerController
import operator
from operator import itemgetter
from datetime import datetime, timedelta


class RoundController:

    def __init__(self, root):
        self.root = root
        self.round_model = Round()
        #self.round_list = list()
        self.round_list1 = list()
        self.round_list2 = list()
        self.round_list3 = list()
        self.round_list4 = list()
        self.pair_list = list()
        self.round_number = None

    def getTime(self):
        date = time.strftime('%d/%m/%y %H:%M:%S', time.localtime())
        return date

    def set_db_players_env(self):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        return players_table

    def set_db_tournaments_env(self):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        return tournaments_table

    def create_round_list(self, tree_frame, selected):
        temp_list = list()
        upper_list = list()
        lower_list = list()
        round_list = list()
        # append tuple tree_frame in a temp list
        for value in tree_frame.item(selected)['values']:
            temp_list.append(value)
        del temp_list[0]
        del temp_list[0]
        i = 0
        while i < 10:
            if i < 5:
                upper_list.append(temp_list[i])
            else:
                lower_list.append(temp_list[i])
            i += 1

        match = (upper_list, lower_list)
        round_list.insert(selected, match)
        return round_list

    def get_players_values(self, tree_frame, score1_spin_box, score2_spin_box, tournaments_table, players_table, selected):

        # ================ Get row rank & score values converted from str to float=======================
        # a=list dict Joueur1 a[0]=dict Joueur1
        a = players_table.search(where('first_name') == self.tree_frame.set((int(selected)), '#3'))
        previous_score1 = float(self.tree_frame.set((int(selected)), '#7'))
        b = players_table.search(where('first_name') == self.tree_frame.set((int(selected)), '#8'))  # Joueur2
        previous_score2 = float(self.tree_frame.set((int(selected)), '#12'))

        # Get new score from spinbox
        score1 = float(score1_spin_box.get())
        score2 = float(score2_spin_box.get())

        # Display new scores
        tree_frame.set(selected, '#6', score1)  # score match
        tree_frame.set(selected, '#11', score2)

        sum1 = previous_score1 + score1
        sum2 = previous_score2 + score2

        tree_frame.set(selected, '#7', sum1)  # (#4 ou colonne 'scores_class1')
        tree_frame.set(selected, '#12', sum2)

        # Reg total in db
        players_table.update({'score': sum1},
                             where('first_name') == self.tree_frame.set((int(selected)), '#3'))  # Nom Joueur1
        players_table.update({'score': sum2},
                             where('first_name') == self.tree_frame.set((int(selected)), '#8'))  # Nom Joueur2

    def add_valid_button_action(self, input_list, rd_frame, tree_frame,score1_spin_box, score2_spin_box,
                                                            tournament_name,  valid_button1, start_date):

        tournaments_table = self.set_db_tournaments_env()
        players_table = self.set_db_players_env()

        self.tree_frame = tree_frame
        selected = int(self.tree_frame.focus())

        round_number = self.tree_frame.set(selected, '#1')
        if round_number == 'Round1':
            self.get_players_values(tree_frame, score1_spin_box,
                                    score2_spin_box, tournaments_table, players_table, selected)
            self.round_list1.append(self.create_round_list(tree_frame, selected))

            if selected == 3:
                self.round_list1.insert(0, round_number)
                self.round_list1.insert(1, start_date)
                self.round_list1.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.round_model.all_tournament_rounds_list.append(self.round_list1)

        elif round_number == 'Round2':
            round_number = self.tree_frame.set(selected, '#1')
            self.get_players_values(self.tree_frame, score1_spin_box, score2_spin_box, tournaments_table,
                                                      players_table, selected)
            self.round_list2.append(self.create_round_list(tree_frame, selected))

            if selected == 7:
                self.round_list2.insert(0, round_number)
                self.round_list2.insert(1, start_date)
                self.round_list2.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.round_model.all_tournament_rounds_list.append(self.round_list2)

        elif round_number == 'Round3':

            self.get_players_values(tree_frame, score1_spin_box, score2_spin_box, tournaments_table,
                                                      players_table, selected)
            self.round_list3.append(self.create_round_list(tree_frame, selected))

            if selected == 11:
                self.round_list3.insert(0, round_number)
                self.round_list3.insert(1, start_date)
                self.round_list3.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.round_model.all_tournament_rounds_list.append(self.round_list3)

        elif round_number == 'Round4':
            self.get_players_values(tree_frame, score1_spin_box, score2_spin_box, tournaments_table,
                                                      players_table, selected)
            self.round_list4.append(self.create_round_list(tree_frame, selected))

            if selected == 15:
                self.round_list4.insert(0, round_number)
                self.round_list4.insert(1, start_date)
                self.round_list4.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.round_model.all_tournament_rounds_list.append(self.round_list4)

        tournaments_table.update({'rounds_lists': self.round_model.all_tournament_rounds_list}, where('tournament_name') == tournament_name)

    def match_data(self):
        self.round_model.players_list = self.round_model.create_players_list()
        self.sort_players()
        self.create_upper_and_lower_list()
        return self.create_match()

    def sort_players(self):
        """Sort players by ranking"""
        self.round_model.players_list.sort(key=lambda x: x.ranking, reverse=True)
        # print(self.round_model.players_list)

    def create_upper_and_lower_list(self):
        length = len(self.round_model.players_list)
        i = 0
        while i < length:
            if i < length / 2:
                self.round_model.upper_list.append(self.round_model.players_list[i])
            else:
                self.round_model.lower_list.append(self.round_model.players_list[i])
            i += 1

    def create_match(self):
        length = len(self.round_model.players_list)
        i = 0
        while i < length / 2:
            list_1 = [self.round_model.lower_list[i].id, 0]
            list_2 = [self.round_model.upper_list[i].id, 0]
            match = (list_1, list_2)
            self.round_model.matches_list.append(match)
            i += 1
        return self.round_model.matches_list

    def quit_round_window(self):
        self.rd_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()

    def init_first_round(self, tournament_name, round_number):  # Return first round player list sorted by rank
        self.tournament_name = tournament_name
        players_table = RoundController.set_db_players_env(self)  # Appel de la fonction depuis roundView-> gen_round1
        serialized_players = []
        serialized_players = players_table.search(where('tournament_name') == self.tournament_name)
        serialized_players.sort(key=operator.itemgetter('rank'), reverse=True)  # Tri suivant le rang
        round_players_list = list()

        i = 0
        init_list = list()
        while i < len(serialized_players):  # Liste comprenant [id, nom, prénom, rang] ===> treeview
            init_list = [
                serialized_players[i].get('first_name'),
                serialized_players[i].get('last_name'),
                serialized_players[i].get('rank'),
                0.0,
                serialized_players[i].get('score')]

            round_players_list.insert(i, init_list)  # Insertion first_list à l'indice i
            i += 1
        return round_players_list

    """
    def init_second_round(self, tournament_name):   # Return second round player list sorted by rank & score
        self.tournament_name = tournament_name
        players_table = self.set_db_players_env()       # Appel de la fonction depuis RoundController
        serialized_players = []
        serialized_players = players_table.search(where('tournament_name') == self.tournament_name)

        serialized_players.sort(key=operator.itemgetter('rank'), reverse=True)  # Tri suivant le rang
        serialized_players.sort(key=operator.itemgetter('score'), reverse=True)  # Tri suivant le score

        round_players_list = list()    # liste de dico_players

        i = 0
        while i < len(serialized_players):  # Liste comprenant [nom, prénom,rang, score, total] ===> treeview +1 pour ajout total
            init_list = [
                            serialized_players[i].get('first_name'),
                            serialized_players[i].get('last_name'),
                            int(serialized_players[i].get('rank')),
                            0.0,
                            float(serialized_players[i].get('score'))
                            ]
            round_players_list.insert(i, init_list)  # Insertion first_list à l'indice i
            i += 1
        #print("list_serial_p", list_serial_players)
        return round_players_list
    """

    # Initialisation rounds 3 & 4
    def init_rounds(self, tournament_name, round_number):
        self.tournament_name = tournament_name
        players_table = self.set_db_players_env()
        serialized_players = []
        serialized_players = players_table.search(where('tournament_name') == self.tournament_name)

        # Round1
        if round_number == 1:
            serialized_players.sort(key=operator.itemgetter('rank'), reverse=True)  # Tri suivant le rang

        # Round2
        elif round_number == 2:
            serialized_players.sort(key=operator.itemgetter('rank'), reverse=True)  # Tri suivant le rang
            serialized_players.sort(key=operator.itemgetter('score'), reverse=True)  # Tri suivant le score

        # Rounds 3,4
        else:
            serialized_players.sort(key=operator.itemgetter('score'), reverse=True)  # Tri suivant le score
            round_players_list = list()  # liste de dico_players

        round_players_list = list()  # liste de dico_players

        i = 0
        while i < len(serialized_players):  # Liste comprenant [nom, prénom,rang] ===> treeview
            init_list = [
                serialized_players[i].get('first_name'),
                serialized_players[i].get('last_name'),
                int(serialized_players[i].get('rank')),
                0.0,
                float(serialized_players[i].get('score'))
            ]
            round_players_list.insert(i, init_list)  # Insertion first_list à l'indice i
            i += 1

        return round_players_list


















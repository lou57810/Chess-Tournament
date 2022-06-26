from tinydb import TinyDB, Query, where
import tkinter as tk
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import ttk as tk

from model.round import Round
import operator
from operator import itemgetter
from datetime import datetime, timedelta


class RoundController:

    def __init__(self, root):
        self.root = root
        self.round_list = list()
        self.pair_list = list()
        self.round_number = None
        self.match_list = list()
        self.match = tuple()
        self.round_model = Round()

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

    def reg_players_values(self, tree_frame, selected):  # Reg in db
        players_table = self.set_db_players_env()

        # ================ Get row rank & score values converted from str to float=======================
        elt = int(selected) - 3

        while elt <= int(selected):
            previous_score1 = players_table.search(where('first_name') == tree_frame.set((int(elt)), '#4'))[0]["score"]
            previous_score2 = players_table.search(where('first_name') == tree_frame.set((int(elt)), '#9'))[0]["score"]

            score1 = float(tree_frame.set((int(elt)), '#7'))
            score2 = float(tree_frame.set((int(elt)), '#12'))

            sum1 = float(previous_score1) + score1
            sum2 = float(previous_score2) + score2

            tree_frame.set(elt, '#8', float(sum1))  # (#4 ou colonne 'scores_class1')
            tree_frame.set(elt, '#13', float(sum2))

            players_table.update({'score': float(sum1)}, where('first_name') == tree_frame.set(elt,
                                                                                               '#4'))  # & where('tournament_name') == str(tree_frame.set(elt), '#1'))  # Nom Joueur1
            players_table.update({'score': float(sum2)},
                                 where('first_name') == tree_frame.set(elt, '#9'))  # Nom Joueur2
            elt += 1

    def reg_round_matches(self, tree_frame, start_date, selected):
        round_list = []
        elt = int(selected) - 3
        while elt <= int(selected):
            match_list1 = list()
            match_list2 = list()

            match_list1.append(tree_frame.set(elt, '#4') + ' ' + tree_frame.set(int(elt), '#5'))
            match_list1.append(tree_frame.set(elt, '#7'))

            match_list2.append(tree_frame.set(elt, '#9') + ' ' + tree_frame.set(int(elt), '#10'))
            match_list2.append(tree_frame.set(elt, '#12'))

            match = (match_list1, match_list2)
            round_list.append(match)
            elt += 1

        return round_list

    def insert_round_datas(self, round_list, round_number, start_date):
        round_list.insert(0, round_number)
        round_list.insert(1, start_date)
        round_list.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.round_model.all_tournament_rounds_list.append(round_list)

    def valid_round(self, tree_frame, start_date, tournament_name):
        tournaments_table = self.set_db_tournaments_env()
        round_list = list()
        selected = tree_frame.focus()
        round_name = tree_frame.set(int(selected), '#2')

        if round_name == 'Round1':
            self.reg_players_values(tree_frame, selected)
            round_list = self.reg_round_matches(tree_frame, start_date, selected)

            if int(selected) == 3:
                self.insert_round_datas(round_list, round_name, start_date)

        elif round_name == 'Round2':
            self.reg_players_values(tree_frame, selected)
            round_list = self.reg_round_matches(tree_frame, start_date, selected)

            if int(selected) == 7:
                self.insert_round_datas(round_list, round_name, start_date)

        elif round_name == 'Round3':
            self.reg_players_values(tree_frame, selected)
            round_list = self.reg_round_matches(tree_frame, start_date, selected)
            if int(selected) == 11:
                self.insert_round_datas(round_list, round_name, start_date)

        elif round_name == 'Round4':
            self.reg_players_values(tree_frame, selected)
            round_list = self.reg_round_matches(tree_frame, start_date, selected)
            if int(selected) == 15:
                self.insert_round_datas(round_list, round_name, start_date)

            tournaments_table.update({'rounds_lists': self.round_model.all_tournament_rounds_list},
                                     where('tournament_name') == tournament_name)

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

    # Initialisation rounds
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

# ==========================Button fct==========================
    def get_score1(self, input_list, tree_frame):
        selected = tree_frame.focus()
        round_number = self.get_round_number(tree_frame, selected)
        row = (int(round_number) * 4) - 1
        if int(selected) < row:
            self.select_row(tree_frame, int(selected) + 1)  # Auto pass to following row
        # Display new scores
        score1 = 1.0
        score2 = 0.0
        tree_frame.set(selected, '#7', score1)  # score match
        tree_frame.set(selected, '#12', score2)  # score match

    def get_score_equal(self, input_list, tree_frame):
        selected = tree_frame.focus()
        round_number = self.get_round_number(tree_frame, selected)
        row = (int(round_number) * 4) - 1
        if int(selected) < row:
            self.select_row(tree_frame, int(selected) + 1)  # Auto pass to following row
        # Display new scores
        score1 = 0.5
        score2 = 0.5

        tree_frame.set(selected, '#7', score1)  # score match
        tree_frame.set(selected, '#12', score2)  # score match

    def get_score2(self, input_list, tree_frame):
        selected = tree_frame.focus()
        round_number = self.get_round_number(tree_frame, selected)
        row = (int(round_number) * 4) - 1
        if int(selected) < row:
            self.select_row(tree_frame, int(selected) + 1)  # Auto pass to following row
        # Display new scores
        score1 = 0.0
        score2 = 1.0

        tree_frame.set(selected, '#7', score1)  # score match
        tree_frame.set(selected, '#12', score2)  # score match

    def select_row(self, tree_frame, row):
        tree_frame.focus(row)
        tree_frame.selection_set(row)

    def get_round_number(self, tree_frame, selected):
        round_name = tree_frame.set(int(selected), '#2')
        round_number = int(round_name[5])
        return round_number


















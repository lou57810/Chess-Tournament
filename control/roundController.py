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
        self.round_model = Round()
        self.round_list = list()
        self.round_list1 = list()
        self.round_list2 = list()
        self.round_list3 = list()
        self.round_list4 = list()
        self.pair_list = list()
        self.round_number = None
        self.match_list = list()
        self.match = tuple()

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
    """
    def create_row_round_list(self, tree_frame, selected):
        temp_list = list()
        upper_list = list()
        lower_list = list()
        round_list = list()
        # append tuple tree_frame in a temp list
        #for child in tree_frame.get_children():
        for value in tree_frame.item(selected)['values']:
            temp_list.append(value)
        del temp_list[0]    # Tournament, Match
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
    

    def create_round_list(self, tree_frame, selected):
        temp_list = list()
        upper_list = list()
        lower_list = list()
        round_list = list()
        # append tuple tree_frame in a temp list
        for value in tree_frame.item(selected)['values']:
            temp_list.append(value)
        #print("temp_list:", temp_list)
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
        """

    def reg_players_values(self, tree_frame):  # Reg in db
        players_table = self.set_db_players_env()

        # ================ Get row rank & score values converted from str to float=======================

        for elt in tree_frame.get_children():

            previous_score1 = float(tree_frame.set((int(elt)), '#8'))
            previous_score2 = float(tree_frame.set((int(elt)), '#13'))

            score1 = float(tree_frame.set((int(elt)), '#7'))
            score2 = float(tree_frame.set((int(elt)), '#12'))

            sum1 = previous_score1 + score1
            sum2 = previous_score2 + score2

            tree_frame.set(elt, '#8', previous_score1 + score1)  # (#4 ou colonne 'scores_class1')
            tree_frame.set(elt, '#13', previous_score2 + score2)

            # Reg total in db
            players_table.update({'score': sum1}, where('first_name') == (tree_frame.set(elt, '#4')))# & where('tournament_name') == str(tree_frame.set(elt), '#1'))  # Nom Joueur1
            players_table.update({'score': sum2}, where('first_name') == (tree_frame.set(elt, '#9')))  # Nom Joueur2

    def get_match(self, match):
        i = 0
        match_list = list()
        while i < 4:
            print("Match:", match)
            match_list.append(match)
            print("list:", match_list)
            i += 1


    def reg_round_matches(self, tree_frame):
        round_list = []
        match_list1 = list()
        match_list2 = list()
        match1 = tuple()
        match2 = tuple()
        match3 = tuple()
        match4 = tuple()

        players_table = self.set_db_players_env()
        tournament_name = tree_frame.set(1, '#1')
        print("tournament_name:", tournament_name)
        #elt = 0
        for elt in tree_frame.get_children():
            match_list1.append(tree_frame.set(elt, '#4') + ' ' + tree_frame.set(int(elt), '#5'))
            match_list1.append(tree_frame.set(elt, '#7'))
            match_list2.append(tree_frame.set(elt, '#9') + ' ' + tree_frame.set(int(elt), '#10'))
            match_list2.append(tree_frame.set(elt, '#12'))
            if int(elt) == 0:
                match1 = (match_list1, match_list2)
                print("match1", match1)
                self.round_list.append(match1)
            elif int(elt) == 1:
                match2 = (match_list1, match_list2)
                print("match2", match2)
                self.round_list.append(match2)
            elif int(elt) == 2:
                match3 = (match_list1, match_list2)
                print("match3", match3)
                self.round_list.append(match3)
            elif int(elt) == 3:
                match4 = (match_list1, match_list2)
                print("match4", match4)
                self.round_list.append(match4)




        #self.get_match(match)
        #print("match:", match)
            #print("round_list:", round_list)
            i = 0
            while i < 2:
                del match_list1[0]
                del match_list2[0]
                i += 1
        #round_list = [match1, match2, match3, match4]
        print("round_list:", self.round_list)



    def valid_round(self, tree_frame, start_date):
        #selected = tree_frame.focus()
        temp_list = list()
        temp_list1 = list()
        temp_list2 = list()
        """
            if selected == 3:
                self.round_list1.insert(0, round_number)
                self.round_list1.insert(1, start_date)
                self.round_list1.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.round_model.all_tournament_rounds_list.append(self.round_list1)
        """
        # Db register
        self.reg_players_values(tree_frame)
        #self.create_round_list()
        #round_list = self.create_matchs_list(tree_frame)
        #print("roundnn_list", round_list)
        self.reg_round_matches(tree_frame)


    def valid_round_back(self, input_list, tree_frame, tournament_name, start_date):
        tournaments_table = self.set_db_tournaments_env()
        players_table = self.set_db_players_env()

        self.tree_frame = tree_frame
        selected = int(self.tree_frame.focus())

        round_number = self.tree_frame.set(selected, '#1')
        if round_number == 'Round1':
            self.get_players_values(tree_frame, score1,
                                    score2, tournaments_table, players_table, selected)
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

# ==========================Button fct==========================
    def get_score1(self, input_list, tree_frame):
        selected = tree_frame.focus()
        if int(selected) < 3:
            self.select_row(tree_frame, int(selected) + 1)  # Auto pass to following row
        # Display new scores
        score1 = 1.0
        score2 = 0.0
        tree_frame.set(selected, '#7', score1)  # score match
        tree_frame.set(selected, '#12', score2)  # score match

    def get_score_equal(self, input_list, tree_frame):
        selected = tree_frame.focus()
        if int(selected) < 3:
            self.select_row(tree_frame, int(selected) + 1)  # Auto pass to following row
        # Display new scores
        score1 = 0.5
        score2 = 0.5

        tree_frame.set(selected, '#7', score1)  # score match
        tree_frame.set(selected, '#12', score2)  # score match

    def get_score2(self, input_list, tree_frame):
        selected = tree_frame.focus()
        if int(selected) < 3:
            self.select_row(tree_frame, int(selected) + 1)  # Auto pass to following row
        # Display new scores
        score1 = 0.0
        score2 = 1.0

        tree_frame.set(selected, '#7', score1)  # score match
        tree_frame.set(selected, '#12', score2)  # score match

    def select_row(self, tree_frame,row):
        tree_frame.focus(row)
        tree_frame.selection_set(row)


















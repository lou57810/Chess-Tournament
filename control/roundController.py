from tinydb import TinyDB, Query, where
import tkinter as tk
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import ttk as tk

from model.round import Round
from control.playerController import PlayerController
import operator
from operator import itemgetter
from datetime import datetime, timedelta


class RoundController:

    def __init__(self, root):
        self.root = root
        self.round_model = Round()
        self.round_list1 = list()
        self.round_list2 = list()
        self.round_list3 = list()
        self.round_list4 = list()
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

    def add_valid_button_action(self, input_list, rd_frame, tree_frame,score1_spin_box, score2_spin_box,
                                                            tournament_name,  valid_button1, start_date):

        tournaments_table = self.set_db_tournaments_env()
        players_table = self.set_db_players_env()

        self.round_model.all_rounds_list1 = list()         # liste générique pour toutes les rondes
        self.round_model.lower_list = list()
        self.round_model.upper_list = list()

        self.tree_frame = tree_frame
        selected = self.tree_frame.focus()
        x = selected
        x = int(x)
        # ================ Get row rank & score values converted from str to int & float=================
        temp_list = list()
        # append tuple tree_frame in a temp list
        for value in self.tree_frame.item(selected)['values']:
            temp_list.append(value)
        i = 2
        # fill lower & upper lists
        while i < 10:
            if i < 6:
                self.round_model.upper_list.append(temp_list[i])
            else:
                self.round_model.lower_list.append(temp_list[i])
            i += 1

        self.round_model.upper_list[2] = int(self.round_model.upper_list[2])
        self.round_model.lower_list[2] = int(self.round_model.lower_list[2])

        self.round_model.upper_list[3] = float(self.round_model.upper_list[3])
        self.round_model.lower_list[3] = float(self.round_model.lower_list[3])
        # ================================================================================================

        round_number = self.tree_frame.set(selected, '#1')

        if round_number == 'Round1':
            # Display new scores
            self.tree_frame.set(selected, '#6', score1_spin_box.get())  # (#4 ou colonne 'scores_class1')
            self.tree_frame.set(selected, '#10', score2_spin_box.get())

            # Reg players scores in database
            players_table.update({'score': float(score1_spin_box.get())},
                                 where('first_name') == self.round_model.upper_list[0])  # Joueur1 score = float
            players_table.update({'score': float(score2_spin_box.get())},
                                 where('first_name') == self.round_model.lower_list[0])  # Joueur2

            # Reg round values in database
            up_list = [self.round_model.upper_list[0] + " " + self.round_model.upper_list[1],
                       float(score1_spin_box.get())]
            low_list = [self.round_model.lower_list[0] + " " + self.round_model.lower_list[1],
                       float(score2_spin_box.get())]

            # Create tuple
            match = (up_list, low_list)
            self.round_list1.append(match)

            # Final round_list
            if x == 3:
                self.round_list1.insert(0, round_number)
                self.round_list1.insert(1, start_date)
                self.round_list1.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.round_model.all_tournament_rounds_list.append(self.round_list1)

        elif round_number == 'Round2':
            # Get round1 scores from database
            a = players_table.search(where('first_name') == self.tree_frame.set((int(selected)), '#3'))  # a=list dict Joueur1 a[0]=dict Joueur1
            old_score1 = a[0]['score']
            b = players_table.search(where('first_name') == self.tree_frame.set((int(selected)), '#7'))  # Joueur2
            old_score2 = b[0]['score']

            # Get new score from spinbox
            new_score1 = float(score1_spin_box.get())
            new_score2 = float(score2_spin_box.get())

            sum1 = old_score1 + new_score1
            sum2 = old_score2 + new_score2

            # Display total scores
            self.tree_frame.set(selected, '#6', sum1)  # (#4 ou colonne 'score_class1')
            self.tree_frame.set(selected, '#10', sum2)

            # Reg players scores in database
            players_table.update({'score': sum1}, where('first_name') == self.round_model.upper_list[0])  # Joueur1
            players_table.update({'score': sum2}, where('first_name') == self.round_model.lower_list[0])  # Joueur2

            # MAJ des tuples matchs
            up_list = [self.round_model.upper_list[0] + " " + self.round_model.upper_list[1], float(sum1)]
            low_list = [self.round_model.lower_list[0] + " " + self.round_model.lower_list[1], float(sum2)]
            match = (up_list, low_list)

            self.round_list2.append(match)

            if x == 7:
                self.round_list2.insert(0, round_number)
                self.round_list2.insert(1, start_date)
                self.round_list2.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.round_model.all_tournament_rounds_list.append(self.round_list2)

        elif round_number == 'Round3':
            # Get round1 scores from database
            a = players_table.search(where('first_name') == self.tree_frame.set((int(selected)), '#3'))
            old_score1 = a[0]['score']
            b = players_table.search(where('first_name') == self.tree_frame.set((int(selected)), '#7'))
            old_score2 = b[0]['score']

            # Get new score from spinbox
            new_score1 = float(score1_spin_box.get())
            new_score2 = float(score2_spin_box.get())

            sum1 = old_score1 + new_score1
            sum2 = old_score2 + new_score2

            # Display total scores
            self.tree_frame.set(selected, '#6', sum1)  # (#4 ou colonne 'score_class1')
            self.tree_frame.set(selected, '#10', sum2)

            # Reg players scores in database
            players_table.update({'score': sum1}, where('first_name') == self.round_model.upper_list[0])  # Joueur1
            players_table.update({'score': sum2}, where('first_name') == self.round_model.lower_list[0])  # Joueur2

            # MAJ des tuples matchs
            up_list = [self.round_model.upper_list[0] + " " + self.round_model.upper_list[1], float(sum1)]
            low_list = [self.round_model.lower_list[0] + " " + self.round_model.lower_list[1], float(sum2)]
            match = (up_list, low_list)

            self.round_list3.append(match)

            if x == 11:
                self.round_list3.insert(0, round_number)
                self.round_list3.insert(1, start_date)
                self.round_list3.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.round_model.all_tournament_rounds_list.append(self.round_list3)

        elif round_number == 'Round4':
            # Get round1 scores from database
            a = players_table.search(where('first_name') == self.tree_frame.set((int(selected)), '#3'))
            old_score1 = a[0]['score']
            b = players_table.search(where('first_name') == self.tree_frame.set((int(selected)), '#7'))
            old_score2 = b[0]['score']

            # Get new score from spinbox
            new_score1 = float(score1_spin_box.get())
            new_score2 = float(score2_spin_box.get())

            sum1 = old_score1 + new_score1
            sum2 = old_score2 + new_score2

            # Display total scores
            self.tree_frame.set(selected, '#6', sum1)  # (#4 ou colonne 'score_class1')
            self.tree_frame.set(selected, '#10', sum2)

            # Reg players scores in database
            players_table.update({'score': sum1}, where('first_name') == self.round_model.upper_list[0])  # Joueur1
            players_table.update({'score': sum2}, where('first_name') == self.round_model.lower_list[0])  # Joueur2

            # MAJ des tuples matchs
            up_list = [self.round_model.upper_list[0] + " " + self.round_model.upper_list[1], float(sum1)]
            low_list = [self.round_model.lower_list[0] + " " + self.round_model.lower_list[1], float(sum2)]
            match = (up_list, low_list)

            self.round_list4.append(match)

            if x == 15:
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

    def get_tournament_name(self):
        tournament_name = PlayerController.display_tournament_round_window(t)

    def quit_round_window(self):
        self.rd_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()

    def init_first_round(self, tournament_name):  # Return first round player list sorted by rank
        self.tournament_name = tournament_name
        players_table = RoundController.set_db_players_env(self)  # Appel de la fonction depuis roundView-> gen_round1
        serialized_players = []
        serialized_players = players_table.search(where('tournament_name') == self.tournament_name)

        first_round_list = list()

        i = 0
        first_list = list()
        while i < len(serialized_players):  # Liste comprenant [id, nom, prénom, rang] ===> treeview
            first_list = [
                serialized_players[i].get('first_name'),
                serialized_players[i].get('last_name'),
                serialized_players[i].get('rank'),
                0.0]

            first_round_list.insert(i, first_list)  # Insertion first_list à l'indice i
            i += 1
        res = sorted(first_round_list, key=lambda x:x[2], reverse=True)
        return res

    def init_second_round(self, tournament_name):   # Return second round player list sorted by rank & score
        self.tournament_name = tournament_name
        players_table = self.set_db_players_env()       # Appel de la fonction depuis RoundController
        serialized_players = []
        serialized_players = players_table.search(where('tournament_name') == self.tournament_name)

        serialized_players.sort(key=operator.itemgetter('rank'), reverse=True)  # Tri suivant le rang
        serialized_players.sort(key=operator.itemgetter('score'), reverse=True)  # Tri suivant le score

        list_serial_players = list()    # liste de dico_players

        i = 0
        while i < len(serialized_players):  # Liste comprenant [nom, prénom,rang] ===> treeview
            second_list = [
                            serialized_players[i].get('first_name'),
                            serialized_players[i].get('last_name'),
                            int(serialized_players[i].get('rank')),
                            float(serialized_players[i].get('score'))
                        ]
            list_serial_players.insert(i, second_list)  # Insertion first_list à l'indice i
            i += 1

        return list_serial_players

    def init_rounds(self, tournament_name):
        self.tournament_name = tournament_name
        players_table = self.set_db_players_env()
        serialized_players = []
        serialized_players = players_table.search(where('tournament_name') == self.tournament_name)

        serialized_players.sort(key=operator.itemgetter('score'), reverse=True)  # Tri suivant le score
        list_serial_players = list()  # liste de dico_players

        i = 0
        while i < len(serialized_players):  # Liste comprenant [nom, prénom,rang] ===> treeview
            second_list = [
                serialized_players[i].get('first_name'),
                serialized_players[i].get('last_name'),
                int(serialized_players[i].get('rank')),
                float(serialized_players[i].get('score'))
            ]
            list_serial_players.insert(i, second_list)  # Insertion first_list à l'indice i
            i += 1

        return list_serial_players















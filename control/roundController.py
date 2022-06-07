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
        self.round_list = list()
        self.round_number = 1

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

    def add_valid_button_action(self, input_list, rd_frame, tree_frame,score1_spin_box, score2_spin_box, tournament_name,  valid_button1, start_date):
        self.round_number = 1
        data = list()
        for element in input_list:
            data.append(element.get())

        tournaments_table = self.set_db_tournaments_env()
        players_table = self.set_db_players_env()

        first_round_list = list()
        lower_list = list()
        upper_list = list()
        first_round_list = self.init_first_round(tournament_name)
        self.create_upper_and_lower_list(first_round_list, upper_list, lower_list)

        self.tree_frame = tree_frame
        selected = self.tree_frame.focus()

        # Affiche la valeur du spinbox dans le treeframe
        self.tree_frame.set(selected, '#5', float(score1_spin_box.get()))  # (#4 ou colonne 'score_class1')
        self.tree_frame.set(selected, '#9', float(score2_spin_box.get()))
        x = selected
        x = int(x)

        # Enregistrement des scores joueurs dans la dataBase à chaques itérations
        players_table.update({'score': float(score1_spin_box.get())}, where('first_name') == upper_list[x][0])  # Joueur1
        players_table.update({'score': float(score2_spin_box.get())}, where('first_name') == lower_list[x][0])  # Joueur2

        # Mise à jour des tuples matchs
        up_list = [upper_list[int(x)][0] + " " + upper_list[int(x)][1], float(score1_spin_box.get())]  # id(nom  prénom) + score
        low_list = [lower_list[int(x)][0] + " " + lower_list[int(x)][1], float(score2_spin_box.get())]  # id + score

        # match est un tuple de 2 listes
        match = (up_list, low_list)

        self.round_list.append(match)
        #print("round_list:",self.round_list)

        if x == 3:
            self.round_list.insert(0, 'Round:' + '1')
            self.round_list.insert(1, start_date)
            self.round_list.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            tournaments_table.update({'rounds_lists': self.round_list}, where('tournament_name') == tournament_name)
            self.round_number += 1
            self.get_round_number(self.round_number)

    def match_data(self):
        """Get, sort and separate in two list player's data"""
        self.round_model.players_list = self.round_model.create_players_list()
        self.sort_players()
        self.create_upper_and_lower_list()
        return self.create_match()

    def sort_players(self):
        """Sort players by ranking"""
        self.round_model.players_list.sort(key=lambda x: x.ranking, reverse=True)
        print(self.round_model.players_list)

    def create_upper_and_lower_list(self,first_round_list, upper_list, lower_list):
        length = len(first_round_list)
        i = 0
        while i < length:
            if i < length / 2:
                upper_list.append(first_round_list[i])
            else:
                lower_list.append(first_round_list[i])
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
        print("get_t:",tournament_name)


    def quit_round_window(self):
        # menu_controller = MenuController(self.root)
        # self.menu_controller.clean_window()
        self.rd_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()

    def init_first_round(self, tournament_name):  # Renvoie une liste comprenant (Id, Nom+Prénom, rang)
        self.tournament_name = tournament_name
        players_table = RoundController.set_db_players_env(self)  # Appel de la fonction depuis roundView-> gen_round1
        serialized_players = []
        serialized_players = players_table.search(where('tournament_name') == self.tournament_name)

        first_round_list = list()

        i = 0
        first_list = list()
        while i < len(serialized_players):  # Liste comprenant [id,(nom et prénom),rang] ===> treeview
            first_list = [
                serialized_players[i].get('first_name'),
                serialized_players[i].get('last_name'),
                serialized_players[i].get('rank'),
                '0.0']

            first_round_list.insert(i, first_list)  # Insertion first_list à l'indice i
            i += 1
        res = sorted(first_round_list, key=lambda x:x[2], reverse=True)
        return res

    def init_second_round(self, tournament_name):
        self.tournament_name = tournament_name
        players_table = self.set_db_players_env()       # Appel de la fonction depuis RoundController
        serialized_players = []
        serialized_players = players_table.search(where('tournament_name') == self.tournament_name)
        i = 0
        second_list = list()
        serialized_players.sort(key=operator.itemgetter('rank'), reverse=True)  # Tri suivant le rang
        serialized_players.sort(key=operator.itemgetter('score'), reverse=True)  # Tri suivant le score

        while i < len(serialized_players):  # Liste comprenant [id,(nom et prénom),rang] ===> treeview ordre = id
            challengers = ([serialized_players[i].get('id'),
                            (serialized_players[i].get('first_name') + " " + serialized_players[i].get(
                                'last_name')),
                            serialized_players[i].get('rank'),
                            serialized_players[i].get('score')])
            second_list.insert(i, challengers)
            i += 1

        second_round_list = second_list
        return second_round_list

    def get_round_number(self,r):
        if r is None:
            r = 1
        else:
            self.round_number = r
            print("number:",self.round_number)
            return self.round_number

    def get_round_list2(self, data2):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        Round.j += 1
        if Round.j <= 4:
            Round.round2.append(data2)
        if Round.j == 4:
            Round.all_rounds.append(Round.round2)
            # tournaments_table.update({'rounds_list': Round.all_rounds})  # Round.all_rounds})
            Round.reg_db_rounds(self)










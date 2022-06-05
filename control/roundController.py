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


class RoundController:

    def __init__(self, root):
        self.root = root
        self.round_model = Round()
        self.round_list = list()

    def getTime(self):
        date = time.strftime('%d/%m/%y %H:%M:%S', time.localtime())
        return date

    def create_round(self):
        data = ['name', '12:00', '13:00']
        data.append(self.match_data())
        # Retrieve first id not use and add
        data.append(0)
        new_round = Round(data)
        new_round.serialize_round_data()

    def add_valid_button_action(self, input_list, rd_frame, tree_frame,score1_spin_box, score2_spin_box, tournament_name,  valid_button1):

        data = list()
        data_check = True
        for element in input_list:
            print("elt_input_list :",element.get())
            data.append(element.get())
            #data.append('0')  # score
            if not element.get():
                data_check = False
        if data_check:
            #data.append('0')  # score
            print("data:",data)
            #round = Round(data)
            #round.serialize_round_data()
            #round.write_data()
        # pass
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        tournaments_table = db.table('tournaments')
        #serialized_players = players_table.all()
        first_round_list = list()
        lower_list = list()
        upper_list = list()
        first_round_list = self.init_first_round(tournament_name)
        print("valid_tournament_name:", tournament_name)
        i = 0
        while i < len(first_round_list) / 2:
            upper_list.append(first_round_list[int(i)])
            i += 1

        i = len(first_round_list) / 2
        i = int(i)
        while i < len(first_round_list):
            lower_list.append(first_round_list[int(i)])
            i += 1
        self.tree_frame = tree_frame
        selected = self.tree_frame.focus()
        print("x1:",selected)
        # Affiche la valeur du spinbox dans le treeframe
        self.tree_frame.set(selected, '#5', float(score1_spin_box.get()))  # (#4 ou colonne 'score_class1')
        self.tree_frame.set(selected, '#9', float(score2_spin_box.get()))
        x = selected
        x = int(x)
        print("x2:", x)

        # Enregistrement des scores joueurs dans la dataBase à chaques itérations
        players_table.update({'score': float(score1_spin_box.get())}, where('first_name') == upper_list[x][0])  # Joueur1
        players_table.update({'score': float(score2_spin_box.get())}, where('first_name') == lower_list[x][0])  # Joueur2


        # Mise à jour des tuples matchs
        up_list = [upper_list[int(x)][0] + " " + upper_list[int(x)][1], float(score1_spin_box.get())]  # id(nom  prénom) + score
        low_list = [lower_list[int(x)][0] + " " + lower_list[int(x)][1], float(score2_spin_box.get())]  # id + score



        # match est un tuple de 2 listes
        match = (up_list, low_list)

        self.round_list.append(match)
        print("round_list:",self.round_list)

        if x == 3:
            self.round_list.insert(0, 'Round:' + '1')
            tournaments_table.update({'rounds_lists': self.round_list}, where('tournament_name') == tournament_name)
            print("round_list:", self.round_list)

    def get_round_list(self, data1):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')


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

    def create_upper_and_lower_list(self):
        """Split players in two list"""
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
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        #serialized_players = players_table.all()
        serialized_players = []
        serialized_players = players_table.search(where('tournament_name') == self.tournament_name)

        first_round_list = list()
        #print("firstRoundList:",first_round_list)
        i = 0
        challengers = list()
        while i < len(serialized_players):  # Liste comprenant [id,(nom et prénom),rang] ===> treeview
            challengers = [
                serialized_players[i].get('first_name'),
                serialized_players[i].get('last_name'),
                serialized_players[i].get('rank'),
                '0.0']

            first_round_list.insert(i, challengers)  # Insertion challengers à l'indice i
            i += 1
        res = sorted(first_round_list, key=lambda x:x[2])
        print("res:", res)
        return res


       










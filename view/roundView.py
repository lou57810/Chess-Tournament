import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import ttk as tk
# from datetime import *
from tinydb import TinyDB, Query, where
from tkinter import messagebox
from datetime import datetime, timedelta
from model.player import Player
# from control.controller import Controller
from model.round import Round
from model.tournament import Tournament
from control.tournamentController import TournamentController
from control.playerController import PlayerController
from control.roundController import RoundController

import operator


class RoundView:
    round_list = []
    round_list1 = []
    round_list2 = []
    data_player_list2 = []

    def __init__(self, root, round_list=list()):  # ,round_list
        self.root = root
        self.round_list = round_list
        self.tree_frame = None
        self.rd_frame = None
        self.tournament_name = None
        self.ROUND_FIELDS = ("matchs", "first_name1", "last_name1", "rank1", "score1", "first_name2",
                             "last_name2", "rank2", "score2")
        self.player_controller = PlayerController(self.root)
        self.round_controller = RoundController(self.root)
        count = 0

    def display_round_window(self):

        self.r_frame = Frame(self.root)
        self.tree_frame = ttk.Treeview(self.r_frame)
        self.r_frame.pack(padx=5, pady=20)

        # ===========================Style & frames=============================
        style = ttk.Style()
        # Pick a theme        
        style.theme_use("alt")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white"
                        )
        # Change selected color
        style.map("Treeview", background=[("selected", "brown")])

        tree_scroll = Scrollbar(self.r_frame)
        tree_scroll.config(command=self.tree_frame.yview)
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.tree_frame = ttk.Treeview(self.r_frame, yscrollcommand=tree_scroll.set, select="extended")
        self.tree_frame.pack(pady=20)

        # Define Columns        
        self.tree_frame["columns"] = self.ROUND_FIELDS
        self.tree_frame.column('#0', width=0, stretch=NO)
        self.tree_frame.heading('#0', text='', anchor=CENTER)

        # Create Striped Row Tags
        self.tree_frame.tag_configure('oddrow', background="#ecdab9")
        self.tree_frame.tag_configure('evenrow', background="#a47053")

        for elt in self.ROUND_FIELDS:
            self.tree_frame.column(elt, anchor=CENTER, width=100)
            self.tree_frame.heading(elt, text=elt, anchor=CENTER)
        

        # ================Add Management Entries Boxes==========================

    def round_data_set(self, tournament_name, start_date):
        # Create new frame
        self.rd_frame = Frame(self.root)
        self.rd_frame.pack()

        spin_joueur1_label = Label(self.rd_frame, text="Score class 1")
        spin_joueur1_label.grid(row=1, column=2, padx=0, pady=10)

        spin_joueur2_label = Label(self.rd_frame, text="Score class 2")
        spin_joueur2_label.grid(row=1, column=3, padx=5, pady=10)

        input_list = list()
        
        score1_spin_box = Spinbox(self.rd_frame, values=(0.0, 0.5, 1.0), font=("helvetica", 10), width=4)
        score1_spin_box.grid(row=2, column=2, padx=10, pady=10)
        input_list.append(score1_spin_box)

        score2_spin_box = Spinbox(self.rd_frame, values=(0.0, 0.5, 1.0), font=("helvetica", 10), width=4)
        score2_spin_box.grid(row=2, column=3, padx=10, pady=10)
        input_list.append(score2_spin_box)

           
        valid_button1 = Button(self.rd_frame, text="Valider",
                                       command=lambda: self.round_controller.add_valid_button_action(input_list,
                                        self.rd_frame, self.tree_frame, score1_spin_box, score2_spin_box, tournament_name, valid_button1, start_date))
        valid_button1.grid(row=2, column=4, padx=10, pady=20)

        

        quit_button = Button(self.rd_frame, text="Quitter", command=lambda: RoundController.quit_round_window(self))
        quit_button.grid(row=4, column=5, padx=20, pady=20)
    

    # ==========================Database============================

    def create_tournament_db(self):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        tournaments_table = db.table('tournaments')

            
    """
    def init_third_round(self):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        serialized_players = players_table.all()

        thirdList = list()
        serialized_players.sort(key=operator.itemgetter('Classement'), reverse=True)  # Tri suivant le rang
        print("serial:", serialized_players)
        serialized_players.sort(key=operator.itemgetter('score'), reverse=True)  # Tri suivant le score

        i = 0
        while i < len(serialized_players):  # Liste comprenant [id,(nom et prénom),rang] ===> treeview ordre = id
            challengers = ([serialized_players[i].get('id'),
                            (serialized_players[i].get('first_name') + ' ' + serialized_players[i].get(
                                'last_name')),
                            serialized_players[i].get('Classement'),
                            serialized_players[i].get('score')])
            thirdList.insert(i, challengers)
            i += 1

        thirdRoundList = thirdList
        return thirdRoundList
    """
    
    def gen_round1(self, t):
        # Create new frame
        self.rd_frame = Frame(self.root)
        self.rd_frame.pack()        

        lowerList = list()
        upperList = list()
        sorted_round_list = RoundController.init_first_round(self, t)
        
        j = 0
        while j < len(sorted_round_list) / 2:
            upperList.append(sorted_round_list[j])
            j += 1        

        j = int(len(sorted_round_list) / 2)
        while j < len(sorted_round_list):
            lowerList.append(sorted_round_list[j])
            j += 1
        

        # Output to entry boxes
        count = len(self.tree_frame.get_children())

        i = 0
        while i < len(sorted_round_list) / 2:

            if count % 2 == 0:
                self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                    "Match " + str(i + 1),
                    upperList[i][0],  # name
                    upperList[i][1],  # last_name
                    upperList[i][2],  # classement
                    upperList[i][3],  # float(score1_spinBox.get()): score
                    lowerList[i][0],
                    lowerList[i][1],
                    lowerList[i][2],
                    lowerList[i][3],  # float(score2_spinBox.get()),
                    ),
                                           tags=('evenrow',))

            else:
                self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                    "Match " + str(i + 1),
                    upperList[i][0],
                    upperList[i][1],
                    upperList[i][2],
                    upperList[i][3],  # float(score1_spinBox.get()),
                    lowerList[i][0],
                    lowerList[i][1],
                    lowerList[i][2],
                    lowerList[i][3],  # float(score2_spinBox.get()),
                    ),
                                           tags=('oddrow',))
            count += 1
            i += 1

   
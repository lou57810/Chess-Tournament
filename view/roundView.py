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
import time
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
        self.l_frame = None
        self.tournament_name = None
        # self.ROUND_FIELDS = ("Rounds", "matchs", "first_name1", "last_name1", "rank1", "score1", "first_name2",
        # "last_name2", "rank2", "score2")
        self.HEADING_ROUND_FIELDS = ("Tournoi", "Rondes", "Matchs", "Nom joueur1", "Prénom joueur1", "Rang1", "Score1",
                                     "Total1", "Nom joueur2", "Prénom joueur2", "Rang2", "Score2", "Total2")
        self.player_controller = PlayerController(self.root)
        self.round_controller = RoundController(self.root)
        self.start_date = None
        count = 0

    def display_round_window(self):
        self.r_frame = Frame(self.root)
        self.tree_frame = ttk.Treeview(self.r_frame)
        self.r_frame.pack(padx=5, pady=20)

        # ===========================Style & frames=============================
        style = ttk.Style()
        # Pick a theme
        # print(style.theme_names())  : themes disponibles pour Tk
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

        self.tree_frame["columns"] = self.HEADING_ROUND_FIELDS
        self.tree_frame.column('#0', width=0, stretch=NO)
        self.tree_frame.heading('#0', text='', anchor=CENTER)

        # Create Striped Row Tags
        self.tree_frame.tag_configure('oddrow', background="#ecdab9")
        self.tree_frame.tag_configure('evenrow', background="#a47053")

        for elt in self.HEADING_ROUND_FIELDS:
            self.tree_frame.column(elt, anchor=CENTER, width=95)
            self.tree_frame.heading(elt, text=elt, anchor=CENTER)

    # ================Add Management Entries Boxes==========================

    def round_data_set(self, tournament_name, start_date):
        # Create new frame
        self.rd_frame = Frame(self.root)
        self.rd_frame.pack()

        input_list = list()

        # spin_joueur1_label = Label(self.rd_frame, text="Score class 1")
        # spin_joueur1_label.grid(row=1, column=2, padx=0, pady=10)

        # spin_joueur2_label = Label(self.rd_frame, text="Score class 2")
        # spin_joueur2_label.grid(row=1, column=3, padx=5, pady=10)

        # score1_spin_box = Spinbox(self.rd_frame, values=(0.0, 0.5, 1.0), font=("helvetica", 10), width=4)
        # score1_spin_box.grid(row=2, column=2, padx=10, pady=10)
        # input_list.append(score1_spin_box)

        # score2_spin_box = Spinbox(self.rd_frame, values=(0.0, 0.5, 1.0), font=("helvetica", 10), width=4)
        # score2_spin_box.grid(row=2, column=3, padx=10, pady=10)
        # input_list.append(score2_spin_box)

        win_button1 = Button(self.rd_frame, text="Joueur1 gagne",
                             command=lambda: self.round_controller.get_score1(input_list, self.tree_frame))

        win_button1.grid(row=2, column=3, padx=10, pady=20)

        win_button_equal = Button(self.rd_frame, text="Egalité",
                                  command=lambda: self.round_controller.get_score_equal(input_list, self.tree_frame))
        win_button_equal.grid(row=2, column=4, padx=10, pady=20)

        win_button2 = Button(self.rd_frame, text="Joueur2 gagne",
                             command=lambda: self.round_controller.get_score2(input_list, self.tree_frame))
        win_button2.grid(row=2, column=5, padx=10, pady=20)

        valid_button = Button(self.rd_frame, text="Validation ronde",
                              command=lambda: self.round_controller.valid_round(self.tree_frame, start_date, tournament_name))
        valid_button.grid(row=2, column=6, padx=10, pady=10)

        # round_button2 = Button(self.rd_frame, text="Deuxième ronde",
        # command=lambda: self.gen_rounds(tournament_name, self.tree_frame))
        # round_button2.grid(row=3, column=5, padx=10, pady=20)

        next_round_button = Button(self.rd_frame, text="Ronde suivante",
                                   command=lambda: self.gen_rounds(tournament_name, self.tree_frame))
        next_round_button.grid(row=3, column=6, padx=10, pady=20)

        quit_button = Button(self.rd_frame, text="Quitter", command=lambda: RoundController.quit_round_window(self))
        quit_button.grid(row=3, column=7, padx=20, pady=20)

    # ==========================Database============================

    def gen_round1(self, tournament_name):  # , round_number):
        # Create new frame
        round_number = 1
        self.rd_frame = Frame(self.root)
        self.rd_frame.pack()
        round_list = list()
        lowerList = list()
        upperList = list()
        sorted_round_list = RoundController.init_first_round(self, tournament_name, round_number)

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

        # fonction saisie des matchs  id players [id_joueur1, id_joueur2] reversible !!! auto
        # fonction avec exeptions

            if count % 2 == 0:
                self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                    tournament_name,
                    "Round" + str(round_number),
                    "Match " + str(i + 1),
                    upperList[i][0],  # name
                    upperList[i][1],  # last_name
                    upperList[i][2],  # classement
                    0.0,  # float(score1_spinBox.get()): score
                    0.0,  # Total
                    lowerList[i][0],
                    lowerList[i][1],
                    lowerList[i][2],
                    0.0,  # float(score2_spinBox.get()),
                    0.0,  # Total
                ),
                                       tags=('evenrow',))

            else:
                self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                    tournament_name,
                    "Round" + str(round_number),
                    "Match " + str(i + 1),
                    upperList[i][0],
                    upperList[i][1],
                    upperList[i][2],
                    0.0,  # float(score1_spinBox.get()),
                    0.0,  # Total
                    lowerList[i][0],
                    lowerList[i][1],
                    lowerList[i][2],
                    0.0,  # float(score2_spinBox.get()),
                    0.0,  # Total
                ),
                                       tags=('oddrow',))
            count += 1
            i += 1

        # self.round_controller.select_row(self.tree_frame, 0)  # Préselectionne row in round tree_frame
        # self.tree_frame.focus(0)
        # self.tree_frame.selection_set(0)
        # self.tree_frame.selection_set(iid=0)  # Does work

    def gen_rounds(self, tournament_name, tree_frame):
        self.tree_frame = tree_frame
        round_list = list()

        # Get n° of round_number
        last_in_tree_frame = len(self.tree_frame.get_children()) - 1
        string_number = str(self.tree_frame.set(last_in_tree_frame, '#2'))
        round_number = int(string_number[5]) + 1

        if round_number == 2:
            tree_round_list = self.round_controller.init_rounds(tournament_name, round_number)
        else:
            tree_round_list = self.round_controller.init_rounds(tournament_name, round_number)

        global count
        count = len(self.tree_frame.get_children())
        j = 0
        i = 0

        while j < len(tree_round_list) / 2:  # 2 iterations
            if count % 2 == 0:
                self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                    tournament_name,
                    "Round" + str(round_number),
                    "Match " + str(count + 1),
                    tree_round_list[i][0],  # nom
                    tree_round_list[i][1],  # prenom
                    tree_round_list[i][2],  # rang
                    tree_round_list[i][3],  # score
                    tree_round_list[i][4],  # total
                    tree_round_list[i + 1][0],
                    tree_round_list[i + 1][1],  # nom2...
                    tree_round_list[i + 1][2],
                    tree_round_list[i + 1][3],
                    tree_round_list[i + 1][4],
                ),
                                       tags=('evenrow',))
            else:
                self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                    tournament_name,
                    "Round" + str(round_number),
                    "Match " + str(count + 1),
                    tree_round_list[i][0],
                    tree_round_list[i][1],
                    tree_round_list[i][2],
                    tree_round_list[i][3],
                    tree_round_list[i][4],
                    tree_round_list[i + 1][0],
                    tree_round_list[i + 1][1],
                    tree_round_list[i + 1][2],
                    tree_round_list[i + 1][3],
                    tree_round_list[i + 1][4],
                ),
                                       tags=('oddrow',))
            count += 1
            i += 2
            j += 1

            round_list.append(tree_round_list)
        return round_list

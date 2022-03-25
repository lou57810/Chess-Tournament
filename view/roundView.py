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
from model.tournament import Tournaments
# from control.tournamentController import TournamentController
import operator


class RoundView:
    round_list = []


    def __init__(self,round_list=list()):
        # self.date = None
        self.round_list = round_list

    def roundView(self, roundFrame):
        # Create a Treeview Frame
        roundFrame = Frame(self.root_window)
        roundFrame.pack(padx=5, pady=20)
        tree_frame = ttk.Treeview(roundFrame)
        round_list = []
        count = 0

        # ==========================Database============================

        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        tournaments_table = db.table('tournaments')

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

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(roundFrame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Scrollbar
        tree_frame = ttk.Treeview(roundFrame, yscrollcommand=tree_scroll.set, select="extended")

        tree_scroll.config(command=tree_frame.yview)

        # Define Columns
        tree_frame["columns"] = (
            "matchs", "player_class1", "player_rank1", "score_class1", "player_class2", "player_rank2",
            "score_class2")

        # Create Striped Row Tags
        tree_frame.tag_configure('oddrow', background="#ecdab9")
        tree_frame.tag_configure('evenrow', background="#a47053")
        tree_frame.pack(padx=50, pady=20)

        # ================= Classement et préparation à l'affichage ===============
        def init_first_round(self):  # Renvoie une liste comprenant (Id, Nom+Prénom, rang)

            serialized_players = players_table.all()
            serialized_players.sort(key=operator.itemgetter('rank'), reverse=True)  # Tri suivant le classement
            firstRoundList = list()

            i = 0
            challengers = list()

            while i < len(serialized_players):  # Liste comprenant [id,(nom et prénom),rang] ===> treeview
                challengers = [serialized_players[i].get('id'),
                               (serialized_players[i].get('first_name') + " " + serialized_players[i].get('last_name')),
                               serialized_players[i].get('rank')]

                firstRoundList.insert(i, challengers)  # Insertion challengers à l'indice i
                i += 1

            return firstRoundList

        # Retourne une liste classée par ordre gagnants(points) et par classement(en cas égalité)
        def init_second_round(self):
            serialized_players = players_table.all()
            # orderedList = getScores(self)   # Liste classée par scores et par rang
            # print("orderedList: ", orderedList)

            challengers = list()
            i = 0
            secondList = list()
            # serialized_players = players_table.all()
            # serialized_players.sort(key=operator.itemgetter('rank'),reverse=True)  # Tri suivant le classement
            while i < len(serialized_players):  # Liste comprenant [id,(nom et prénom),rang] ===> treeview
                challengers = ([serialized_players[i].get('id'),
                                (serialized_players[i].get('first_name') + " " + serialized_players[i].get(
                                    'last_name')),
                                serialized_players[i].get('rank'),
                                serialized_players[i].get('score')])
                secondList.insert(i, challengers)
                i += 1

            score1List = list()
            score05List = list()
            score0List = list()
            i = 0

            # for elt in secondList:
            while i < len(secondList):
                for elt in secondList:
                    if elt[3] == '1':
                        score1List.append(elt)
                        score1List.sort(key=lambda x: x[2], reverse=True)
                    elif elt[3] == '0.5':
                        score05List.append(elt)
                        score05List.sort(key=lambda x: x[2], reverse=True)
                    elif elt[3] == '0':
                        score0List.append(elt)
                        score0List.sort(key=lambda x: x[2], reverse=True)
                    i += 1

            secondRoundList = list()
            secondRoundList = score1List + score05List + score0List
            return secondRoundList

        # Répartition affichage dans le treeview depuis la db
        def gen_round1(self):
            tournaments_table = db.table('tournaments')
            serialized_players = players_table.all()

            firstRoundList = list()
            lowerList = list()
            upperList = list()
            firstRoundList = init_first_round(self)

            i = 0
            while i < len(firstRoundList) / 2:
                upperList.append(firstRoundList[i])
                i += 1

            i = int(len(firstRoundList) / 2)
            while i < len(firstRoundList):
                lowerList.append(firstRoundList[i])
                i += 1

            global count

            tree_frame.tag_configure('oddrow', background="#ecdab9")
            tree_frame.tag_configure('evenrow', background="#a47053")
            # Output to entry boxes
            count = len(tree_frame.get_children())

            i = 0
            while i < len(firstRoundList) / 2:

                if count % 2 == 0:
                    tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                        "Match " + str(i + 1),
                        upperList[i][1],
                        upperList[i][2],
                        score1_spinBox.get(),
                        lowerList[i][1],
                        lowerList[i][2],
                        score2_spinBox.get(),
                    ),
                                      tags=('evenrow',))

                else:
                    tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                        "Match " + str(i + 1),
                        upperList[i][1],
                        upperList[i][2],
                        score1_spinBox.get(),
                        lowerList[i][1],
                        lowerList[i][2],
                        score2_spinBox.get(),
                    ),
                                      tags=('oddrow',))
                count += 1
                i += 1

            s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tournaments_table.update({'start_time': s})

        # ===========Validation des entrées scores button: Valider1==================
        def update_player_table1(self):
            # db = TinyDB('data/db_tournaments.json')
            # tournaments_table = db.table('tournaments')

            first_round_list = list()
            lower_list = list()
            upper_list = list()
            match = ()

            first_round_list = init_first_round(self)
            i = 0

            while i < len(first_round_list) / 2:
                upper_list.append(first_round_list[int(i)])
                i += 1

            i = len(first_round_list) / 2

            i = int(i)
            while i < len(first_round_list):
                lower_list.append(first_round_list[int(i)])
                i += 1

            x = tree_frame.focus()
            print("x:", x)
            # Affiche la valeur du spinbox dans le treeframe
            tree_frame.set(x, '#4', score1_spinBox.get())  # (#4 ou colonne 'score_class1')
            tree_frame.set(x, '#7', score2_spinBox.get())
            x = int(x)

            # Enregistrement des scores joueurs dans la dataBase à chaques itérations
            players_table.update({'score': score1_spinBox.get()}, where('id') == upper_list[x][0])
            players_table.update({'score': score2_spinBox.get()}, where('id') == lower_list[x][0])

            up_list = [upper_list[int(x)][1], score1_spinBox.get()]  # id + score
            low_list = [lower_list[int(x)][1], score2_spinBox.get()]  # id + score

            # match est un tuple de 2 listes
            match = (up_list, low_list)
            round_list.append(match)
            print("Match: ", match)
            print("x_end:", x)
            print("round_list: ",round_list)
            reg_db_round(self,round_list)

        def gen_round2():
            tree_frame.tag_configure('oddrow', background="#ecdab9")
            tree_frame.tag_configure('evenrow', background="#a47053")
            global count
            secondRoundList = list()
            secondRoundList = init_second_round(self)
            count = len(tree_frame.get_children())
            print("secondRoundList: ", secondRoundList)
            j = 0
            i = 0
            while j < len(secondRoundList) / 2:  # 2 iterations
                if count % 2 == 0:
                    tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                        "Match " + str(count + 1),
                        secondRoundList[i][1],  # nom
                        secondRoundList[i][2],  # rang
                        secondRoundList[i][3],  # score
                        secondRoundList[i + 1][1],  # nom2...
                        secondRoundList[i + 1][2],
                        secondRoundList[i + 1][3],
                    ),
                                      tags=('evenrow',))
                else:
                    tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                        "Match " + str(count + 1),
                        secondRoundList[i][1],
                        secondRoundList[i][2],
                        secondRoundList[i][3],
                        secondRoundList[i + 1][1],
                        secondRoundList[i + 1][2],
                        secondRoundList[i + 1][3],
                    ),
                                      tags=('oddrow',))
                count += 1
                i += 2
                j += 1

        def clear_all_Records():
            # Clear the treeview
            for record in tree_frame.get_children():
                tree_frame.delete(record)

        def quitRoundWindow():
            roundFrame.destroy()


        def updateAndSaveRound2():
            secondRoundList = list()
            secondRoundList = Round.initSecondRound(self)
            i = 0
            x = tree_frame.selection()[0]
            # tree_frame.delete(x)
            print("xxx: ", int(x))

            x = int(x)
            y = x
            if x == 1:
                y += 1
            if x == 2:
                y += 2
            if x == 3:
                y += 3
            X = y + 1

            if x % 2 == 0:
                tree_frame.insert(parent="", index=int(x), iid=int(x), text="", values=(
                    "Match " + str(x + 1),
                    secondRoundList[y][0],
                    secondRoundList[y][1],  # nom                      # rang
                    score1_spinBox.get(),
                    secondRoundList[X][0],
                    secondRoundList[X][1],
                    score2_spinBox.get(),), tags=('evenrow',))  # Score
                print("x :", x)
                print("X :", X)

            else:
                tree_frame.insert(parent="", index=int(x), iid=int(x), text="", values=(
                    "Match " + str(x + 1),
                    secondRoundList[y][0],  # id
                    secondRoundList[y][1],  # nom                      # rang
                    score1_spinBox.get(),
                    secondRoundList[X][0],  # id
                    secondRoundList[X][1],  # nom                      # rang
                    score2_spinBox.get(),), tags=('oddrow',))
                print("x :", x)
                print("X :", X)

        def clear_Entries():
            score1_spinBox.delete(0, END)
            score2_spinBox.delete(0, END)

        def reg_db_round(self,round_list):
            tournaments_table.update({'rounds_list': round_list})

        def get_end_round():
            e = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tournaments_table.update({'end_time': e})

        # =====================Fill the Treeview======================

        # Format columns
        tree_frame.column("#0", width=0, stretch=NO)
        tree_frame.column("matchs", anchor=W, width=50)
        tree_frame.column("player_class1", anchor=CENTER, width=200)
        tree_frame.column("player_rank1", anchor=CENTER, width=50)
        tree_frame.column("score_class1", anchor=CENTER, width=50)
        tree_frame.column("player_class2", anchor=CENTER, width=200)
        tree_frame.column("player_rank2", anchor=CENTER, width=50)
        tree_frame.column("score_class2", anchor=CENTER, width=50)

        # Create headings
        tree_frame.heading("#0", text="", anchor=W)
        tree_frame.heading("matchs", text="Matchs", anchor=W)
        tree_frame.heading("player_class1", text="Joueur class1", anchor=CENTER)
        tree_frame.heading("player_rank1", text="Elo", anchor=CENTER)
        tree_frame.heading("score_class1", text="Score", anchor=CENTER)
        tree_frame.heading("player_class2", text="Joueur class2", anchor=CENTER)
        tree_frame.heading("player_rank2", text="Elo", anchor=CENTER)
        tree_frame.heading("score_class2", text="Score", anchor=CENTER)

        # ================Add Management Entries Boxes==========================

        data_frame = LabelFrame(roundFrame, text="Gestion des rondes")
        data_frame.pack(fill="x", padx=30, pady=20)

        gen1_button = Button(data_frame, text="Générer ronde 1",command=lambda: gen_round1(self))
        gen1_button.grid(row=1, column=0, padx=10, pady=20)



        gen234_button = Button(data_frame, text="Générer ronde 234", command=gen_round2)
        gen234_button.grid(row=2, column=0, padx=10, pady=20)

        spinWhite_label = Label(data_frame, text="Score class 1")
        spinWhite_label.grid(row=1, column=2, padx=0, pady=10)
        score1_spinBox = Spinbox(data_frame, values=(0, 0.5, 1), font=("helvetica", 10), width=4)
        score1_spinBox.grid(row=2, column=2, padx=10, pady=10)

        spinBlack_label = Label(data_frame, text="Score class 2")
        spinBlack_label.grid(row=1, column=3, padx=5, pady=10)
        score2_spinBox = Spinbox(data_frame, values=(0, 0.5, 1), font=("helvetica", 10), width=4)
        score2_spinBox.grid(row=2, column=3, padx=10, pady=10)

        valid_button1 = Button(data_frame, text="Valider1", command=lambda: update_player_table1(self))
        valid_button1.grid(row=1, column=4, padx=10, pady=20)

        valid_button2 = Button(data_frame, text="Valider2", command=updateAndSaveRound2)
        valid_button2.grid(row=2, column=4, padx=10, pady=20)

        clear_all_button = Button(data_frame, text="Effacer", command=clear_all_Records)
        clear_all_button.grid(row=4, column=3, padx=10, pady=20)

        test_button = Button(data_frame, text="Enregistrer la ronde",command=reg_db_round(self,round_list))
        test_button.grid(row=4, column=4, padx=10, pady=20)

        regRoundButton = Button(data_frame,text="Cloturer",command=get_end_round)
        regRoundButton.grid(row=5, column=4, padx=10, pady=20)

        quit_button = Button(data_frame, text="Quitter", command=quitRoundWindow)
        quit_button.grid(row=4, column=5, padx=20, pady=20)

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

        round_number = self.round_controller.round_number

        round_label = Label(self.rd_frame, text="ROUND"+str(round_number), font=("Helvetica", 14), foreground='#9a031e')
        round_label.grid(row=1, column=5,padx=10, pady=10)

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

        round_button2 = Button(self.rd_frame, text="Deuxième ronde", command=lambda: self.gen_round2(tournament_name))  # , command=lambda: update_player_table2(self))
        round_button2.grid(row=3, column=5, padx=10, pady=20)

        next_round_button = Button(self.rd_frame, text="Rondes suivantes")  # , command=lambda: update_player_table3(self))
        next_round_button.grid(row=3, column=6, padx=10, pady=20)


        quit_button = Button(self.rd_frame, text="Quitter", command=lambda: RoundController.quit_round_window(self))
        quit_button.grid(row=3, column=7, padx=20, pady=20)

    # ==========================Database============================
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

    # Répartition affichage dans le treeview depuis la db
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

    def gen_round2(self, tournament_name):
        global count

        second_round_list = self.round_controller.init_second_round(tournament_name)

        count = len(self.tree_frame.get_children())
        print("secondRoundList: ", second_round_list)
        j = 0
        i = 0
        while j < len(second_round_list) / 2:  # 2 iterations
            if count % 2 == 0:
                self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                    "Match " + str(count + 1),
                    second_round_list[i][0],
                    second_round_list[i][1],  # nom
                    second_round_list[i][2],  # rang
                    second_round_list[i][3],
                    second_round_list[i + 1][0],
                    second_round_list[i + 1][1],  # nom2...
                    second_round_list[i + 1][2],
                    second_round_list[i + 1][3],
                ),
                                       tags=('evenrow',))
            else:
                self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
                    "Match " + str(count + 1),
                    second_round_list[i][0],
                    second_round_list[i][1],
                    second_round_list[i][2],
                    second_round_list[i][3],
                    second_round_list[i + 1][0],
                    second_round_list[i + 1][1],
                    second_round_list[i + 1][2],
                    second_round_list[i + 1][3],
                ),
                                       tags=('oddrow',))
            count += 1
            i += 2
            j += 1

        data2 = "Round2"
        data2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #RoundController.get_round_list2(self, data2)

    """

    def update_player_table2(self):
        self.tree_frame = RoundView.round_view(self)
        lower_list = list()
        upper_list = list()
        second_round_list = init_second_round(self)

        # print("second_round_list",second_round_list)

        i = 0
        while i < len(second_round_list) / 2:
            upper_list.append(second_round_list[int(i)])
            i += 1

        i = len(second_round_list) / 2
        i = int(i)
        while i < len(second_round_list):
            lower_list.append(second_round_list[int(i)])
            i += 1

        # Affiche la valeur du spinbox dans le treeframe
        y = int(tree_frame.focus())
        print("y:", y)
        val_origin1 = tree_frame.set(y, '#5')
        val1 = float(score1_spinBox.get()) + float(val_origin1)
        self.tree_frame.set(y, '#5', val1)  # (#4 ou colonne 'score_class1')

        val_origin2 = tree_frame.set(y, '#9')
        val2 = float(score2_spinBox.get()) + float(val_origin2)
        self.tree_frame.set(y, '#9', val2)  # score2_spinBox.get())

        data = tree_frame.item(y)
        d = list(data.values())

        tuple_id_score1 = (d[2][1], d[2][4])
        tuple_id_score2 = (d[2][5], d[2][8])
        RoundView.data_player_list2.append(tuple_id_score1)
        RoundView.data_player_list2.append(tuple_id_score2)

        # Enregistrement des scores joueurs dans la dataBase à chaques itérations
        # Mise à jour des tuples matchs

        up_list = [upper_list[y - 5][1], val1]  # id + score
        # print("up_list",up_list)
        low_list = [lower_list[y - 5][1], val2]  # id + score
        # print("low_list", low_list)

        # match est un tuple de 2 listes
        match = (up_list, low_list)
        RoundView.round_list2.append(match)

        if y == 7:
            Round.get_round_player_scores(self, RoundView.data_player_list2)
            data2 = RoundView.round_list2
            Round.get_round_list2(self, data2)

            data2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Round.get_round_list2(self, data2)
    

    def update_player_table3(self):
        # roundFrame = Frame(self.root_window)
        # tree_frame = ttk.Treeview(roundFrame)
        self.tree_frame = RoundView.round_view(self)
        lower_list = list()
        upper_list = list()
        third_round_list = RoundView.init_third_round(self)

        i = 0
        while i < len(third_round_list) / 2:
            upper_list.append(third_round_list[int(i)])
            i += 1

        i = len(third_round_list) / 2
        i = int(i)
        while i < len(third_round_list):
            lower_list.append(third_round_list[int(i)])
            i += 1

        # Affiche la valeur du spinbox dans le treeframe
        z = tree_frame.focus()
        print("z:", z)
        val_origin31 = tree_frame.set(z, '#5')
        val31 = float(score1_spinBox.get()) + float(val_origin31)
        self.tree_frame.set(z, '#5', val31)  # (#4 ou colonne 'score_class1')

        val_origin32 = tree_frame.set(z, '#9')
        val32 = float(score2_spinBox.get()) + float(val_origin32)
        self.tree_frame.set(z, '#9', val32)  # score2_spinBox.get())

        data = tree_frame.item(z)
        d = list(data.values())

        tuple_id_score1 = (d[2][1], d[2][4])
        tuple_id_score2 = (d[2][5], d[2][8])
        RoundView.data_player_list2.append(tuple_id_score1)
        RoundView.data_player_list2.append(tuple_id_score2)

        # Enregistrement des scores joueurs dans la dataBase à chaques itérations
        # Mise à jour des tuples matchs

        up_list = [upper_list[float(y) - 5][1], val1]  # id + score
        # print("up_list",up_list)
        low_list = [lower_list[float(y) - 5][1], val2]  # id + score
        # print("low_list", low_list)

        # match est un tuple de 2 listes
        match = (up_list, low_list)
        RoundView.round_list2.append(match)

        if z == 7:
            Round.get_round_player_scores(self, RoundView.data_player_list2)
            data2 = RoundView.round_list2
            Round.get_round_list2(self, data2)

            data2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Round.get_round_list2(self, data2)
       

    def remove_one_Round(self):
        self.tree_frame = RoundView.round_view(self)
        msg = messagebox.askyesno("Nouvelle ronde!")
        if msg == 1:
            # Clear the treeview
            for elt in self.tree_frame.get_children():
                self.tree_frame.delete(elt)

    

    def reg_db_round(self):
        for elt in tree_frame.get_children():
            print("elt: ", elt)
            print("scores1 :", tree_frame.set(elt, '#4'), tree_frame.set(elt, '#7'))
            # val_origin1 = tree_frame.set(elt, '#4')

    def quitRoundWindow(self):
        self.r_frame = Frame(self.root)
        self.r_frame.destroy()



    def clear_all_Records(self):
        self.tree_frame = RoundView.round_view(self)
        # Clear the treeview
        for record in self.tree_frame.get_children():
            self.tree_frame.delete(record)
    """
    

    # def clear_Entries():
    # score1_spinBox.delete(0, END)
    # score2_spinBox.delete(0, END)


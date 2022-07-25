import tkinter as tk
from tkinter import Button
from tkinter import Frame
from tkinter import Scrollbar
from tkinter import ttk
from control.playerController import PlayerController
from control.roundController import RoundController
from datetime import datetime


class RoundView:

    def __init__(self, root):
        self.root = root
        self.tree_frame = None
        self.rd_frame = None
        self.r_frame = None

        self.HEADING_ROUND_FIELDS = ("Tournoi", "Rondes",
                                     "Matchs", "Nom joueur1",
                                     "Prénom joueur1", "Rang1",
                                     "Score1", "Total1",
                                     "Nom joueur2", "Prénom joueur2",
                                     "Rang2", "Score2", "Total2")
        self.player_controller = PlayerController(self.root)
        self.round_controller = RoundController(self.root)
        self.start_date = None

    def display_round_window(self, tournament_name):
        self.round_controller.switch_window(tournament_name)

        self.r_frame = Frame(self.root)
        self.tree_frame = ttk.Treeview(self.r_frame)
        self.r_frame.pack(padx=5, pady=20)

        # ================= Style & frames ==============
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
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_frame = ttk.Treeview(
            self.r_frame, yscrollcommand=tree_scroll.set, select="extended")
        self.tree_frame.pack(pady=20)

        self.tree_frame["columns"] = self.HEADING_ROUND_FIELDS
        self.tree_frame.column('#0', width=0, stretch=tk.NO)
        self.tree_frame.heading('#0', text='', anchor=tk.CENTER)

        # Create Striped Row Tags
        self.tree_frame.tag_configure('oddrow', background="#ecdab9")
        self.tree_frame.tag_configure('evenrow', background="#a47053")

        for elt in self.HEADING_ROUND_FIELDS:
            self.tree_frame.column(elt, anchor=tk.CENTER, width=95)
            self.tree_frame.heading(elt, text=elt, anchor=tk.CENTER)

    def gen_rounds(self, tournament_name, tree_frame):
        self.tree_frame = tree_frame
        self.rd_frame = Frame(self.root)
        self.rd_frame.pack()

        self.round_controller.start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.round_controller.set_start_date(self.start_date)

        if len(self.tree_frame.get_children()) == 0:
            round_number = 1

        else:
            # Get next n° of round_number
            last_in_tree_frame = len(self.tree_frame.get_children()) - 1
            round_name = str(self.tree_frame.set(last_in_tree_frame, '#2'))
            round_number = int(round_name[5]) + 1

        tree_round_list = self.round_controller.init_rounds(tournament_name, round_number)
        print("tree_round_list", tree_round_list)

        global count
        count = len(self.tree_frame.get_children())
        j = 0
        i = 0

        while j < len(tree_round_list) / 2:  # 2 iterations
            if count % 2 == 0:
                self.tree_frame.insert(
                    parent="", index="end", iid=count, text="", values=(
                        tree_round_list[i][0],  # tournament_name
                        "Round" + str(round_number),
                        "Match " + str(count + 1),
                        tree_round_list[i][1],  # nom1
                        tree_round_list[i][2],  # prenom1
                        tree_round_list[i][3],  # rang
                        tree_round_list[i][4],  # score
                        tree_round_list[i][5],  # total
                        tree_round_list[i + 1][1],  # nom2
                        tree_round_list[i + 1][2],  # prenom2...
                        tree_round_list[i + 1][3],
                        tree_round_list[i + 1][4],
                        tree_round_list[i + 1][5],
                    ),
                    tags=('evenrow',))
            else:
                self.tree_frame.insert(
                    parent="", index="end", iid=count, text="", values=(
                        tree_round_list[i][0],  # tournament_name
                        "Round" + str(round_number),
                        "Match " + str(count + 1),
                        tree_round_list[i][1],
                        tree_round_list[i][2],
                        tree_round_list[i][3],
                        tree_round_list[i][4],
                        tree_round_list[i][5],
                        tree_round_list[i + 1][1],
                        tree_round_list[i + 1][2],
                        tree_round_list[i + 1][3],
                        tree_round_list[i + 1][4],
                        tree_round_list[i + 1][5],
                    ),
                    tags=('oddrow',))
            count += 1
            i += 2
            j += 1

    # ================Add Management Entries Boxes==========================
    def round_data_set(self, tournament_name):
        self.display_round_window(tournament_name)
        self.gen_rounds(tournament_name, self.tree_frame)
        # Create new frame
        self.rd_frame = Frame(self.root)
        self.rd_frame.pack()
        input_list = list()

        win_button1 = Button(
            self.rd_frame, text="Joueur1 gagne",
            command=lambda: self.get_score1(
                input_list, self.tree_frame))

        win_button1.grid(row=2, column=3, padx=10, pady=20)

        win_button_equal = Button(
            self.rd_frame, text="Egalité",
            command=lambda: self.get_score_equal(
                input_list, self.tree_frame))
        win_button_equal.grid(row=2, column=4, padx=10, pady=20)

        win_button2 = Button(
            self.rd_frame, text="Joueur2 gagne",
            command=lambda: self.get_score2(
                input_list, self.tree_frame))
        win_button2.grid(row=2, column=5, padx=10, pady=20)

        valid_button = Button(
            self.rd_frame, text="Validation ronde",
            command=lambda: self.round_controller.valid_round(
                self.tree_frame, tournament_name))
        valid_button.grid(row=2, column=6, padx=10, pady=10)

        next_round_button = Button(
            self.rd_frame, text="Ronde suivante",
            command=lambda: self.gen_rounds(tournament_name, self.tree_frame))
        next_round_button.grid(row=3, column=6, padx=10, pady=20)

        quit_button = Button(
            self.rd_frame, text="Quitter",
            command=lambda: RoundController.quit_round_window(self))
        quit_button.grid(row=3, column=7, padx=20, pady=20)

    def get_score1(self, input_list, tree_frame):
        selected = tree_frame.focus()
        round_number = self.get_round_number(tree_frame, selected)
        row = (int(round_number) * 4) - 1
        if int(selected) < row:
            self.select_row(
                tree_frame, int(selected) + 1)  # Auto pass to following row
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
            self.select_row(
                tree_frame, int(selected) + 1)  # Auto pass to following row
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
            self.select_row(
                tree_frame, int(selected) + 1)  # Auto pass to following row
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

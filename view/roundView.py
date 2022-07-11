import tkinter as tk
from tkinter import Button
from tkinter import Frame
from tkinter import Scrollbar
from tkinter import ttk
from control.playerController import PlayerController
from control.roundController import RoundController


class RoundView:
    round_list = []
    round_list1 = []
    round_list2 = []
    data_player_list2 = []

    def __init__(self, root, round_list=list()):  # round_list
        self.root = root
        self.round_list = round_list
        self.tree_frame = None
        self.rd_frame = None
        self.l_frame = None
        self.r_frame = None
        self.tournament_name = None

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

    # ================Add Management Entries Boxes==========================
    def round_data_set(self, tournament_name):
        self.display_round_window(tournament_name)
        self.round_controller.gen_rounds(tournament_name, self.tree_frame)
        # Create new frame
        self.rd_frame = Frame(self.root)
        self.rd_frame.pack()
        input_list = list()

        win_button1 = Button(
            self.rd_frame, text="Joueur1 gagne",
            command=lambda: self.round_controller.get_score1(
                input_list, self.tree_frame))

        win_button1.grid(row=2, column=3, padx=10, pady=20)

        win_button_equal = Button(
            self.rd_frame, text="Egalité",
            command=lambda: self.round_controller.get_score_equal(
                input_list, self.tree_frame))
        win_button_equal.grid(row=2, column=4, padx=10, pady=20)

        win_button2 = Button(
            self.rd_frame, text="Joueur2 gagne",
            command=lambda: self.round_controller.get_score2(
                input_list, self.tree_frame))
        win_button2.grid(row=2, column=5, padx=10, pady=20)

        valid_button = Button(
            self.rd_frame, text="Validation ronde",
            command=lambda: self.round_controller.valid_round(
                self.tree_frame, tournament_name))
        valid_button.grid(row=2, column=6, padx=10, pady=10)

        next_round_button = Button(
            self.rd_frame, text="Ronde suivante",
            command=lambda: self.round_controller.gen_rounds(tournament_name, self.tree_frame))
        next_round_button.grid(row=3, column=6, padx=10, pady=20)

        quit_button = Button(
            self.rd_frame, text="Quitter",
            command=lambda: RoundController.quit_round_window(self))
        quit_button.grid(row=3, column=7, padx=20, pady=20)

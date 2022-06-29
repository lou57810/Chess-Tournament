import tkinter as tk
from tkinter import *
from tkinter import ttk
import PIL
from PIL import ImageTk, Image
from tkinter import messagebox
from tkcalendar import *

from tinydb import TinyDB, Query, where

from control.playerController import PlayerController
from control.menuController import MenuController
from control.tournamentController import TournamentController
from control.roundController import RoundController

from model.round import Round
from model.player import Player


class PlayerView:
    def __init__(self, root):

        self.ALL_PLAYER_FIELDS = ('tournament_name', 'first_name', 'last_name', 'birth_date', 'gender', 'rank', 'score')
        self.PLAYER_FIELDS = ('Nom du tournoi', 'Nom', 'Prénom', 'Date de naissance', 'Genre', 'Classement', 'Score')
        self.DATA_FIELDS = ('Nom', 'Prénom', 'Date de naissance', 'Genre', 'Classement')
        self.root = root
        self.tree_frame = None
        self.date = None
        self.p_frame = None
        self.player_controller = PlayerController(self.root)
        self.round_controller = RoundController(self.root)

    def display_player_window(self):
        self.p_frame = Frame(self.root)
        self.p_frame.pack(padx=20, pady=20)

        self.tree_frame = ttk.Treeview(self.p_frame)

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
        style.map("Treeview", background=[("selected", "blue")])

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(self.p_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Scrollbar
        self.tree_frame = ttk.Treeview(self.p_frame, yscrollcommand=tree_scroll.set, select="extended")
        self.tree_frame.pack(pady=20)
        tree_scroll.config(command=self.tree_frame.yview)

        # Define Columns
        self.tree_frame["columns"] = self.PLAYER_FIELDS

        self.tree_frame.column('#0', width=0, stretch=NO)
        self.tree_frame.heading('#0', text='', anchor=CENTER)

        self.tree_frame.tag_configure('oddrow', background="white")
        self.tree_frame.tag_configure('evenrow', background="lightblue")

        for element in self.PLAYER_FIELDS:
            self.tree_frame.column(element, anchor=CENTER, width=120)
            self.tree_frame.heading(element, text=element, anchor=CENTER)

    def call_tournament_player_list(self, tournament_name):
        # Depuis tournamentController: Affiche la liste des joueurs si elle existe
        self.display_player_window()
        # Display datas
        players_table = self.round_controller.set_db_players_env()      # Initialise db tournament
        players_table.update({'score': 0.0}, where('tournament_name') == tournament_name)
        tournament_players_data = players_table.search(where('tournament_name') == tournament_name)

        count = 0
        for player in tournament_players_data:
            attributes_player = list()

            for element in self.ALL_PLAYER_FIELDS:
                attributes_player.append(player.get(element))
            if count % 2 == 0:
                self.tree_frame.insert('', 'end', text='', values=attributes_player,
                                           tags='evenrow')
            else:
                self.tree_frame.insert('', 'end', text='', values=attributes_player,
                                           tags='oddrow')
            count += 1
        self.tree_frame.pack(padx=20, pady=20)

    def player_data_set(self, tournament_name):  # Enregistre la saisie dans le tournoi
        # Create new frame
        self.p_frame = Frame(self.root)
        self.p_frame.pack()
        """
        def clear_entries():
            f_name_box.delete(0, END)
            l_name_box.delete(0, END)
            date_box.delete(0, 'end')
            gender_var.set(None)  # gender.deselect() don't work
            class_spin_box.delete(0, END)
        """

        # Row number
        y = 0
        input_list = list()

        # Loop for fields names
        for element in self.DATA_FIELDS:
            current_element = StringVar()
            current_element.set(element)

            # Create label
            element_label = Label(self.p_frame, text=element)
            element_label.grid(row=1, column=y)
            # Next row
            y += 1

            if element == 'Nom':
                f_name_box = Entry(self.p_frame, width=25)
                f_name_box.grid(row=2, column=0, padx=10, pady=10)
                input_list.append(f_name_box)

            elif element == 'Prénom':
                l_name_box = Entry(self.p_frame, width=25)
                l_name_box.grid(row=2, column=1, padx=10, pady=10)
                input_list.append(l_name_box)

            elif element == 'Date de naissance':
                date_box = DateEntry(self.p_frame, width=15, locale='fr_FR', selectmode='day', date_pattern='dd/MM/yyyy')
                date_box.grid(row=2, column=2, padx=10, pady=10)
                input_list.append(date_box)

            elif element == "Genre":
                gender_frame = Frame(self.p_frame)
                gender_var = StringVar()
                gender_var.set("None")

                radiobutton1 = Radiobutton(gender_frame, text="Homme", variable=gender_var, value="Homme")
                radiobutton2 = Radiobutton(gender_frame, text="Femme", variable=gender_var, value="Femme")
                radiobutton1.pack(side=LEFT, padx=15)
                radiobutton2.pack(side=RIGHT, padx=15)
                gender_frame.grid(row=2, column=3)
                input_list.append(gender_var)

            elif element == 'Classement':
                class_spin_box = Spinbox(self.p_frame, from_=0, to=1000, font=("helvetica", 10), width=5)
                input_list.append(class_spin_box)
                class_spin_box.grid(row=2, column=4, padx=10, pady=10)

        # Next column
        y += 1

        # Buttons for management player
        add_player_button = Button(self.p_frame, text="Ajouter joueur",  command=lambda:
                            [self.player_controller.add_player_tree_frame(input_list, self.p_frame,
                            self.tree_frame, y, tournament_name, add_player_button,
                            self.DATA_FIELDS), self.player_controller.clear_entries(f_name_box, l_name_box, date_box, gender_var, radiobutton1,
                      radiobutton2, class_spin_box)])
        add_player_button.grid(row=3, column=0, padx=10, pady=10)

        select_player_button = Button(self.p_frame, text="Selectionner un joueur",
                                      command=lambda: self.player_controller.select_one_record(
                                      self.tree_frame, f_name_box, l_name_box, date_box, gender_var, radiobutton1,
                                      radiobutton2, class_spin_box))
        select_player_button.grid(row=4, column=0, padx=10, pady=10)

        modify_player_button = Button(self.p_frame, text="Modifier",
                                      command=lambda: self.player_controller.modify_one_record(
                                      self.tree_frame, f_name_box, l_name_box, date_box, gender_var, radiobutton1,
                                      radiobutton2, class_spin_box, tournament_name))
        modify_player_button.grid(row=4, column=1, padx=10, pady=10)

        delete_player_button = Button(self.p_frame, text="Supprimer un joueur",
                                      command=lambda: self.player_controller.delete_one_player_button(
                                      self.tree_frame))
        delete_player_button.grid(row=3, column=1, padx=10, pady=10)

        delete_all_players_button = Button(self.p_frame, text="Supprimer tous les joueurs",
                                           command=lambda: self.player_controller.delete_all_players_button
                                           (self.tree_frame))
        delete_all_players_button.grid(row=3, column=2, padx=10, pady=10)

        quit_button = Button(self.p_frame, text="Quitter",
                             command=lambda: PlayerController.quit_player_window(self))
        quit_button.grid(row=3, column=5, padx=10, pady=20)

        gen_rounds = Button(self.p_frame, text="Création Rondes",
                            command=lambda: PlayerController.display_tournament_round_window(self, tournament_name))
        gen_rounds.grid(row=3, column=3, padx=10, pady=20)

        # Bind the treeview
        #self.tree_frame.bind("<ButtonRelease-1>", lambda event: self.player_controller.select_one_record(self.tree_frame, f_name_box, l_name_box, date_box, radiobutton1,
                                      #radiobutton2, class_spin_box, event))







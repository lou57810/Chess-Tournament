import tkinter as tk
from tkinter import Button
from tkinter import ttk
from tkinter import Entry
from tkinter import Label
from tkcalendar import DateEntry
from tkinter import Frame
from tkinter import Scrollbar
from tkinter import Spinbox
from tkinter import Radiobutton
from tinydb import where
from control.playerController import PlayerController
from view.roundView import RoundView
from model.dbInterface import Interface
from model.player import Player


class PlayerView:
    def __init__(self, root):

        self.ALL_PLAYER_FIELDS = ('tournament_name', 'first_name',
                                  'last_name', 'birth_date',
                                  'gender', 'rank', 'score')
        self.PLAYER_FIELDS = ('Nom du tournoi', 'Nom',
                              'Prénom', 'Date de naissance',
                              'Genre', 'Classement', 'Score')
        self.DATA_FIELDS = (
            'Nom', 'Prénom',
            'Date de naissance',
            'Genre', 'Classement')
        self.root = root
        self.tree_frame = None
        self.date = None
        self.p_frame = None
        self.player_controller = PlayerController(self.root)
        self.round_view = RoundView(self.root)
        self.model_interface = Interface()
        self.model_player = Player()

    def display_player_window(self):
        self.p_frame = Frame(self.root)
        self.p_frame.pack(padx=20, pady=20)

        self.tree_frame = ttk.Treeview(self.p_frame)

        # ======== Style & frames =========
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
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Scrollbar
        self.tree_frame = ttk.Treeview(
            self.p_frame, yscrollcommand=tree_scroll.set, select="extended")
        self.tree_frame.pack(pady=20)
        tree_scroll.config(command=self.tree_frame.yview)

        # Define Columns
        self.tree_frame["columns"] = self.PLAYER_FIELDS

        self.tree_frame.column('#0', width=0, stretch=tk.NO)
        self.tree_frame.heading('#0', text='', anchor=tk.CENTER)

        self.tree_frame.tag_configure('oddrow', background="white")
        self.tree_frame.tag_configure('evenrow', background="lightblue")

        for element in self.PLAYER_FIELDS:
            self.tree_frame.column(element, anchor=tk.CENTER, width=120)
            self.tree_frame.heading(element, text=element, anchor=tk.CENTER)

    def call_tournament_player_list(self, tournament_name):
        self.display_player_window()
        # Display datas
        players_table = self.model_interface.set_db_players_env()
        players_table.update(
            {'score': 0.0}, where('tournament_name') == tournament_name)
        tournament_players_data = players_table.search(
            where('tournament_name') == tournament_name)
        # Récuperer le model et implementer le tout dans une fonction.
        count = 0
        for player in tournament_players_data:
            attributes_player = list()

            for element in self.ALL_PLAYER_FIELDS:
                attributes_player.append(player.get(element))
            if count % 2 == 0:
                self.tree_frame.insert('', 'end', text='', values=attributes_player, tags='evenrow')
            else:
                self.tree_frame.insert('', 'end', text='', values=attributes_player, tags='oddrow')
            count += 1
        self.tree_frame.pack(padx=20, pady=20)

    # Enregistre la saisie dans le tournoi
    def player_data_set(self, tournament_name):
        # Create new frame
        self.p_frame = Frame(self.root)
        self.p_frame.pack()
        # Row number
        y = 0
        input_list = list()

        # Loop for fields names
        for element in self.DATA_FIELDS:
            current_element = tk.StringVar()
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
                date_box = DateEntry(
                    self.p_frame, width=15, locale='fr_FR', selectmode='day',
                    date_pattern='dd/MM/yyyy')
                date_box.grid(row=2, column=2, padx=10, pady=10)
                input_list.append(date_box)

            elif element == "Genre":
                gender_frame = Frame(self.p_frame)
                gender_var = tk.StringVar()
                gender_var.set("None")

                radiobutton1 = Radiobutton(
                    gender_frame, text="Homme",
                    variable=gender_var, value="Homme")
                radiobutton2 = Radiobutton(
                    gender_frame, text="Femme",
                    variable=gender_var, value="Femme")
                radiobutton1.pack(side=tk.LEFT, padx=15)
                radiobutton2.pack(side=tk.RIGHT, padx=15)
                gender_frame.grid(row=2, column=3)
                input_list.append(gender_var)

            elif element == 'Classement':
                class_spin_box = Spinbox(
                    self.p_frame, from_=0, to=1000,
                    font=("helvetica", 10), width=5)
                input_list.append(class_spin_box)
                class_spin_box.grid(row=2, column=4, padx=10, pady=10)

        # Next column
        y += 1

        # Buttons for management player
        add_player_button = Button(
            self.p_frame, text="Ajouter joueur", command=lambda:
            [self.add_player_tree_frame(
                input_list, self.p_frame, self.tree_frame,
                y, tournament_name, add_player_button,
                self.DATA_FIELDS),
                self.clear_entries(
                f_name_box, l_name_box, date_box, gender_var, radiobutton1,
                radiobutton2, class_spin_box)])
        add_player_button.grid(row=3, column=0, padx=10, pady=10)

        select_player_button = Button(
            self.p_frame, text="Selectionner un joueur",
            command=lambda: self.select_one_record(
                self.tree_frame, f_name_box, l_name_box,
                date_box, gender_var, radiobutton1,
                radiobutton2, class_spin_box))
        select_player_button.grid(row=4, column=0, padx=10, pady=10)

        modify_player_button = Button(
            self.p_frame, text="Modifier",
            command=lambda: self.modify_one_record(
                self.tree_frame, f_name_box, l_name_box,
                date_box, gender_var, radiobutton1,
                radiobutton2, class_spin_box, tournament_name))
        modify_player_button.grid(row=4, column=1, padx=10, pady=10)

        delete_player_button = Button(
            self.p_frame, text="Supprimer un joueur",
            command=lambda: self.delete_one_player_button(self.tree_frame))
        delete_player_button.grid(row=3, column=1, padx=10, pady=10)

        delete_all_players_button = Button(
            self.p_frame, text="Supprimer tous les joueurs",
            command=lambda: self.player_controller.delete_all_players_button(self.tree_frame))
        delete_all_players_button.grid(row=3, column=2, padx=10, pady=10)

        quit_button = Button(
            self.p_frame, text="Quitter",
            command=lambda: PlayerController.quit_player_window(self))
        quit_button.grid(row=3, column=5, padx=10, pady=20)

        gen_rounds = Button(
            self.p_frame, text="Création Rondes", command=lambda: self.round_view.round_data_set(tournament_name))

        gen_rounds.grid(row=3, column=3, padx=10, pady=20)

    def modify_one_record(self, tree_frame, f_name_box, l_name_box, date_box, gender_var,
                          radiobutton1, radiobutton2, class_spin_box, tournament_name):

        players_table = self.model_interface.set_db_players_env()
        for elt in players_table:
            print("players_table:", elt)
        selected = tree_frame.focus()
        value = tree_frame.item(selected, 'values')
        if radiobutton1.invoke == "Homme":
            gender_var = "Homme"
        elif radiobutton2.invoke == "Femme":
            gender_var = "Femme"
        # Updating treeview
        tree_frame.item(selected, text="", values=(
                tournament_name,
                f_name_box.get(),
                l_name_box.get(),
                date_box.get(),
                gender_var.get(),
                class_spin_box.get(),
                value[6]))

        name = f_name_box.get()
        print("name:", name)
        players_table.update({'first_name': f_name_box.get()}, where('first_name') == name)
        players_table.update({'last_name': l_name_box.get()}, where('first_name') == name)
        players_table.update({'birth_date': date_box.get()}, where('first_name') == name)
        players_table.update({'gender': gender_var.get()}, where('first_name') == name)
        players_table.update({'rank': class_spin_box.get()}, where('first_name') == name)
        players_table.update({'score': 0}, where('first_name') == name)

    def select_one_record(self, tree_frame,
                          f_name_box,
                          l_name_box,
                          date_box,
                          gender_var,
                          radiobutton1,
                          radiobutton2,
                          class_spin_box):
        self.clear_entries(f_name_box, l_name_box, date_box, gender_var, radiobutton1, radiobutton2, class_spin_box)
        selected = tree_frame.focus()
        values = tree_frame.item(selected, 'values')

        f_name_box.insert(0, values[1])
        l_name_box.insert(0, values[2])
        date_box.insert(0, values[3])
        if values[4] == "Homme":
            radiobutton1.invoke()
        else:
            radiobutton2.invoke()
        class_spin_box.insert(0, values[5])

    def clear_entries(self, f_name_box, l_name_box, date_box, gender_var, radiobutton1, radiobutton2, class_spin_box):
        f_name_box.delete(0, tk.END)
        l_name_box.delete(0, tk.END)
        date_box.delete(0, tk.END)
        gender_var.set(None)
        class_spin_box.delete(0, tk.END)

    def delete_one_player_button(self, tree_frame):
        player_selected = tree_frame.focus()
        temp = tree_frame.item(player_selected, 'values')
        self.model_player.delete_player_data(temp[1])  # nom du joueur

        for element in tree_frame.selection():
            tree_frame.delete(element)

    def add_player_tree_frame(self, input_list, frame, tree_frame,
                              y, tournament_name, add_player_button,
                              data_fields):
        count = len(tree_frame.get_children())
        data = self.player_controller.reg_tournament_player(tournament_name, input_list, count)

        tree_frame.tag_configure('oddrow', background="white")
        tree_frame.tag_configure('evenrow', background="lightblue")

        if count % 2 == 0:
            tree_frame.insert('', 'end', text='', values=data, tags='evenrow')
        else:
            tree_frame.insert('', 'end', text='', values=data, tags='oddrow')
        count += 1

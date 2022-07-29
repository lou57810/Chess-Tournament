import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
from tkcalendar import DateEntry
from tkinter import Spinbox
from tkinter import Scrollbar
from tkinter import Label
from tkinter import Radiobutton
from control.tournamentController import TournamentController
from control.menuController import MenuController


class TournamentView:
    def __init__(self, root):
        self.root = root
        self.tree_frame = None
        self.t_frame = None
        self.TOURNAMENT_FIELDS = (
            "Nom du tournoi", "Lieu", "Date debut",
            "Date fin", "Nombre tours", "Timing",
            "Description")

        self.tournament_controller = TournamentController(self.root)
        self.menu_controller = MenuController


    def display_tournament_window(self):
        # Create a Treeview Frame
        self.t_frame = Frame(self.root)
        self.t_frame.pack(pady=20)
        self.tree_frame = ttk.Treeview(self.t_frame)

        # ================= Style & frames ===================
        style = ttk.Style()  # Pick a theme
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
        tree_scroll = Scrollbar(self.t_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Scrollbar
        self.tree_frame = ttk.Treeview(
            self.t_frame, yscrollcommand=tree_scroll.set, select="extended")
        self.tree_frame.pack()
        tree_scroll.config(command=self.tree_frame.yview)

        # Define Columns
        self.tree_frame["columns"] = self.TOURNAMENT_FIELDS
        self.tree_frame.column('#0', width=0, stretch=tk.NO)
        self.tree_frame.heading('#0', text='', anchor=tk.CENTER)

        for element in self.TOURNAMENT_FIELDS:
            self.tree_frame.column(element, anchor=tk.CENTER, width=120)
            self.tree_frame.heading(element, text=element, anchor=tk.CENTER)


        # Alternative rows
        self.tree_frame.tag_configure('oddrow', background="white")
        self.tree_frame.tag_configure('evenrow', background="lightblue")

        # Display datas
        all_tournaments_data = self.tournament_controller.read_data()
        i = 0
        count = 0
        index = 0
        for tournament in all_tournaments_data:
            tournament_attributes = []
            for values in vars(tournament).values():
                tournament_attributes.append(values)
                del tournament_attributes[7:]   # Suppression des valeurs inutiles

            if count % 2 == 0:
                self.tree_frame.insert('', 'end', text='', values=tournament_attributes, tags='evenrow')
            else:
                self.tree_frame.insert('', 'end', text='', values=tournament_attributes, tags='oddrow')
            count += 1

        self.tree_frame.pack()

        # ================Add Management Entries Boxes=================

    def tournament_data_set(self):
        self.t_frame = Frame(self.root)
        self.t_frame.pack()

        # Row number
        y = 0
        input_list = list()
        # Loop for fields names
        for element in self.TOURNAMENT_FIELDS:
            current_elt = tk.StringVar()
            current_elt.set(element)  # Création d'un set

            # Create label
            element_label = Label(self.t_frame, text=element)
            element_label.grid(row=0, column=y)

            if element == "Timing":
                speed_frame = Frame(self.t_frame)
                speed_var = tk.StringVar()
                speed_var.set("None")

                bulletRadio = Radiobutton(
                    speed_frame, anchor=tk.W, text="Bullet",
                    variable=speed_var, value="bullet", width=4)
                fastRadio = Radiobutton(
                    speed_frame, anchor=tk.W, text="Rapide",
                    variable=speed_var, value="rapide", width=5)
                blitzRadio = Radiobutton(
                    speed_frame, anchor=tk.W, text="Blitz",
                    variable=speed_var, value="blitz", width=3)
                bulletRadio.pack(anchor=tk.W, side=tk.LEFT, padx=0)
                fastRadio.pack(anchor=tk.W, side=tk.LEFT, padx=0)
                blitzRadio.pack(anchor=tk.W, side=tk.LEFT, padx=0)
                speed_frame.grid(row=2, column=5)
                input_list.append(speed_var)

            elif element == "Date debut":
                start_date_box = DateEntry(
                    self.t_frame, width=15, locale='fr_FR',
                    selectmode='day', date_pattern='dd/MM/yyyy')
                start_date_box.delete(0, tk.END)
                start_date_box.grid(row=1, column=2, padx=1, pady=10)
                input_list.append(start_date_box)

            elif element == 'Date fin':
                end_date_box = DateEntry(
                    self.t_frame, width=15, locale='fr_FR',
                    selectmode='day', date_pattern='dd/MM/yyyy')
                end_date_box.delete(0, tk.END)
                end_date_box.grid(row=1, column=3, padx=1, pady=10)
                input_list.append(end_date_box)

            elif element == "Nom du tournoi":
                name_box = Entry(self.t_frame, width=20)
                name_box.grid(row=1, column=0, padx=10, pady=10)
                input_list.append(name_box)

            elif element == "Lieu":
                place_box = Entry(self.t_frame, width=20)
                place_box.grid(row=1, column=1, padx=10, pady=10)
                input_list.append(place_box)

            elif element == 'Nombre tours':
                count_spinBox = Spinbox(self.t_frame, from_=0, to=100,
                                        font=("helvetica", 10), width=0)
                count_spinBox.grid(row=1, column=4, padx=0, pady=10)
                input_list.append(count_spinBox)

            elif element == "Description":
                descript_box = Entry(self.t_frame, width=20)
                descript_box.grid(row=1, column=6, padx=10, pady=10)
                input_list.append(descript_box)

            y += 1

        # Button for send input to wrapper
        """
        add_tournament_button = Button(self.t_frame, text="Ajouter un tournoi",
                                       command=lambda: [self.tournament_controller.add_tournament_button_action(
                                           input_list, add_tournament_button), self.display_new_tournament()])
        """

        add_tournament_button = Button(self.t_frame, text="Ajouter un tournoi",
                                       command=lambda: [self.display_new_tournament(input_list),
                                                        self.tournament_controller.reg_tournament_data(input_list)])
        add_tournament_button.grid(row=4, column=0, padx=20, pady=20)

        quit_button = Button(
            self.t_frame, text="Quitter",
            command=lambda:
            TournamentController.quit_tournament_window(self))
        quit_button.grid(row=4, column=6, padx=10, pady=20)

        # Bind the players Set
        self.tree_frame.bind('<Double-Button-1>', lambda event: self.tour_db_click())

    def display_new_tournament(self, input_list):
        data = self.tournament_controller.check_new_tournament_data(input_list)

        count = 0
        if count % 2 == 0:
            self.tree_frame.insert('', index='end', iid=0, text='', values=data, tags='evenrow')
        else:
            self.tree_frame.insert('', index='end', iid=0, text='', values=data, tags='evenrow')
        count += 1


    def tour_db_click(self):
        tournament_selected = self.tree_frame.focus()
        temp = self.tree_frame.item(tournament_selected, 'values')
        # TournamentController récupère le nom du tournoi
        TournamentController.display_add_player_window(self, temp[0])



from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tinydb import TinyDB, Query, where
from tkinter import messagebox
from tkinter.messagebox import *
from control.tournamentController import TournamentController
from view.playerView import PlayerView

# from control.controller import Controller
from model.tournament import Tournaments


class TournamentView:
    def __init__(self, root_window):
        self.root_window = root_window


    def tourView(self, tourFrame):
        # Create a Treeview Frame
        tourFrame = Frame(self.root_window)
        tourFrame.pack(pady=20)
        tree_frame = ttk.Treeview(tourFrame)
        # =============Database=================================================
        db = TinyDB('data/db_tournaments.json')
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
        tree_scroll = Scrollbar(tourFrame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Scrollbar
        tree_frame = ttk.Treeview(tourFrame, yscrollcommand=tree_scroll.set, select="extended")
        tree_frame.pack(pady=20)
        tree_scroll.config(command=tree_frame.yview)

        # Define Columns
        tree_frame["columns"] = (
            "tourn_name", "place_name", "start_date", "end_date", "tourns_number", "timing", "description")

        # ============================Fcts===============================

        def add_Entries(self):

            global count
            tournament_data_list = list()
            # Create Striped Row Tags
            tree_frame.tag_configure('oddrow', background="white")
            tree_frame.tag_configure('evenrow', background="lightblue")

            # Output to entry boxes
            count = len(tree_frame.get_children())

            if count % 2 == 0:
                tree_frame.insert(parent="", index=count, iid=count, text="", values=(
                    nameBox.get(),
                    placeBox.get(),
                    startDateBox.get(),
                    endDateBox.get(),
                    count_spinBox.get(),
                    time_shot.get(),
                    descriptBox.get()),
                                  tags=('evenrow',)
                                  )
            else:
                tree_frame.insert(parent="", index=count, iid=count, text="", values=(
                    nameBox.get(),
                    placeBox.get(),
                    startDateBox.get(),
                    endDateBox.get(),
                    count_spinBox.get(),
                    time_shot.get(),
                    descriptBox.get()),
                                  tags=('oddrow',)
                                  )
            count += 1

            db = TinyDB('data/db_tournaments.json')
            tournaments_table = db.table('tournaments')

            serialized_tournament = {
                'tourn_name': nameBox.get(),
                'place_name': placeBox.get(),
                'start_date': startDateBox.get(),
                'end_date': endDateBox.get(),
                'tourns_number': count_spinBox.get(),
                'timing': time_shot.get(),
                'description': descriptBox.get()
            }

            tournaments_table.insert(serialized_tournament)
            # values = tree_frame.item(0, 'values')     Retourne un tuple de valeurs de la ligne
            clear_Entries(self)

        def query_tournament_db(self):
            global count
            count = 0
            tree_frame.tag_configure('oddrow', background="#ecdab9")
            tree_frame.tag_configure('evenrow', background="#a47053")

            # tournaments_table = Tournaments.set_tinyDB_Tournaments(self)
            serialized_tournaments = tournaments_table.all()

            n = 0
            for record in serialized_tournaments:
                if n % 2 == 0:
                    tree_frame.insert(parent="", index=n, iid=n, text='',
                                      values=(
                                          serialized_tournaments[n]['tourn_name'],
                                          serialized_tournaments[n]['place_name'],
                                          serialized_tournaments[n]['start_date'],
                                          serialized_tournaments[n]['end_date'],
                                          serialized_tournaments[n]['tourns_number'],
                                          serialized_tournaments[n]['timing'],
                                          serialized_tournaments[n]['description']),
                                      tags=('evenrow',))

                else:
                    tree_frame.insert(parent="", index=n, iid=n, text='',
                                      values=(
                                          serialized_tournaments[n]['tourn_name'],
                                          serialized_tournaments[n]['place_name'],
                                          serialized_tournaments[n]['start_date'],
                                          serialized_tournaments[n]['end_date'],
                                          serialized_tournaments[n]['tourns_number'],
                                          serialized_tournaments[n]['timing'],
                                          serialized_tournaments[n]['description']),
                                      tags=('oddrow',))
                n += 1

        def update_one_record(self):
            selected = tree_frame.focus()
            # x = tree_frame.selection()[0]
            # records = tournaments_table.all()
            db = TinyDB('data/db_tournaments.json')
            tournaments_table = db.table('tournaments')
            tournaments_table.insert({
                'tourn_name': nameBox.get(),
                'place_name': placeBox.get(),
                'start_date': startDateBox.get(),
                'end_date': endDateBox.get(),
                'tourns_number': count_spinBox.get(),
                'timing': time_shot.get(),
                'description': descriptBox.get()
            })

            el = tournaments_table.all()[int(selected)]
            tournaments_table.remove(doc_ids=[el.doc_id])

            # refresh my_tree
            tree_frame.delete(selected)
            if count % 2 == 0:
                tree_frame.insert(parent="", index=selected, iid=selected, text="", values=(
                    nameBox.get(),
                    placeBox.get(),
                    startDateBox.get(),
                    endDateBox.get(),
                    count_spinBox.get(),
                    time_shot.get(),
                    descriptBox.get()),
                                  tags=('evenrow',)
                                  )
            else:
                tree_frame.insert(parent="", index=selected, iid=selected, text="", values=(
                    nameBox.get(),
                    placeBox.get(),
                    startDateBox.get(),
                    endDateBox.get(),
                    count_spinBox.get(),
                    time_shot.get(),
                    descriptBox.get()),
                                  tags=('oddrow',)
                                  )

        def remove_One_Entry(self):
            clear_Entries(self)
            x = tree_frame.selection()[0]
            tree_frame.delete(x)

            tournaments_table = db.table('tournaments')
            el = tournaments_table.all()[int(x)]
            tournaments_table.remove(doc_ids=[el.doc_id])
            messagebox.showinfo("Deleted!", "Your record is deleted")
            clear_Entries()

        def remove_all_Records(self):
            response = messagebox.askyesno("Cette opératon est irréversible!!")
            tournaments_table = db.table('tournaments')
            if response == 1:
                # Clear the treeview
                for record in tree_frame.get_children():
                    tree_frame.delete(record)
                tournaments_table.truncate()

        def clear_Entries(self):
            nameBox.delete(0, END)
            placeBox.delete(0, END)
            startDateBox.delete(0, END)
            endDateBox.delete(0, END)
            count_spinBox.delete(0, END)
            time_shot.set(None)  # gender.deselect() don't work
            descriptBox.delete(0, END)

            # Selection curseur souris

        def selectEntry(self):
            clear_Entries(self)

            # Grab record Number
            selected = tree_frame.focus()

            # Grab record values
            values = tree_frame.item(selected, 'values')
            nameBox.insert(0, values[0])
            placeBox.insert(0, values[1])
            startDateBox.insert(0, values[2])
            endDateBox.insert(0, values[3])
            count_spinBox.insert(0, values[4])

            # ==========RadioBtn===========
            if values[5] == "bullet":
                bulletRadio.invoke()
            elif values[5] == "blitz":
                blitzRadio.invoke()
            elif values[5] == "rapide":
                fastRadio.invoke()
            # =============================

            descriptBox.insert(0, values[6])

        def tour_db_click(self):
            tournament_selected = tree_frame.focus()
            self.display_playerWindow(self.playerFrame)
            #PlayerView.add_entries(self)



        def quitTourWindow(self):
            tourFrame.destroy()

        # ==============================Fill the Treeview============================

        tree_frame.column("#0", width=0, stretch=NO)
        tree_frame.column("tourn_name", anchor=W, width=130)
        tree_frame.column("place_name", anchor=W, width=130)
        tree_frame.column("start_date", anchor=CENTER, width=130)
        tree_frame.column("end_date", anchor=CENTER, width=130)
        tree_frame.column("tourns_number", anchor=CENTER, width=120)
        tree_frame.column("timing", anchor=CENTER, width=130)
        tree_frame.column("description", anchor=CENTER, width=130)

        # Create headings
        tree_frame.heading("#0", text="", anchor=W)
        tree_frame.heading("tourn_name", text="Nom du tournoi", anchor=CENTER)
        tree_frame.heading("place_name", text="Lieu", anchor=W)
        tree_frame.heading("start_date", text="Date début", anchor=W)
        tree_frame.heading("end_date", text="Date fin", anchor=W)
        tree_frame.heading("tourns_number", text="Nombre de tours", anchor=CENTER)
        tree_frame.heading("timing", text="Choix du temps", anchor=CENTER)
        tree_frame.heading("description", text="Description", anchor=CENTER)

        # ================Add Management Entries Boxes=================

        data_frame = LabelFrame(tourFrame, text="Management Tournois")
        data_frame.pack(fill="x", padx=30, pady=20)

        # Labels
        name_label = Label(data_frame, text="Nom")
        name_label.grid(row=0, column=1, padx=45, pady=10)
        place_label = Label(data_frame, text="Lieu")
        place_label.grid(row=0, column=2, padx=60, pady=10)
        startDate_label = Label(data_frame, text="Date début")
        startDate_label.grid(row=0, column=3, padx=40, pady=10)
        endDate_label = Label(data_frame, text="Date Fin")
        endDate_label.grid(row=0, column=4, padx=40, pady=10)
        count_label = Label(data_frame, text="Nombre de tours")
        count_label.grid(row=0, column=5, padx=10, pady=10)
        descript_label = Label(data_frame, text="Description")
        descript_label.grid(row=0, column=6, padx=5, pady=10)

        # Logical Entry boxes
        nameBox = Entry(data_frame, width=25)
        nameBox.grid(row=1, column=1, padx=10, pady=10)
        placeBox = Entry(data_frame, width=25)
        placeBox.grid(row=1, column=2, padx=10, pady=10)
        startDateBox = DateEntry(data_frame, width=15)
        startDateBox.delete(0, END)
        startDateBox.grid(row=1, column=3, padx=1, pady=10)
        endDateBox = DateEntry(data_frame, width=15)
        endDateBox.delete(0, END)
        endDateBox.grid(row=1, column=4, padx=1, pady=10)
        count_spinBox = Spinbox(data_frame, from_=0, to=100, font=("helvetica", 10), width=2)
        count_spinBox.grid(row=1, column=5, padx=5, pady=10)
        descriptBox = Entry(data_frame, width=25)
        descriptBox.grid(row=1, column=6, padx=10, pady=10)

        # RadioButtons
        time_shot = StringVar()
        time_shot.set(None)

        radio_frame = LabelFrame(tourFrame, text="Choix du temps")

        bulletRadio = Radiobutton(radio_frame, text="Bullet", variable=time_shot, value="bullet", width=10)
        fastRadio = Radiobutton(radio_frame, text="Rapide", variable=time_shot, value="rapide", width=10)
        blitzRadio = Radiobutton(radio_frame, text="Blitz", variable=time_shot, value="blitz", width=10)
        bulletRadio.grid(row=1, column=0, padx=30)
        fastRadio.grid(row=1, column=1, padx=30)
        blitzRadio.grid(row=1, column=2, padx=30)

        radio_frame.pack()

        # ================Button Commands(rm = remove)======================

        button_frame = LabelFrame(tourFrame, text="Commandes")
        button_frame.pack(pady=20)

        add_button = Button(button_frame, text="Ajouter un tournoi", command=lambda: add_Entries(self))
        add_button.grid(row=0, column=0, padx=10, pady=20)

        display_button = Button(button_frame, text="Afficher les tournois", command=lambda: query_tournament_db(self))
        display_button.grid(row=0, column=1, padx=10, pady=20)

        modif_button = Button(button_frame, text="Modifier", command=lambda: update_one_record(self))
        modif_button.grid(row=0, column=2, padx=10, pady=20)

        rm_one_button = Button(button_frame, text="Test", command=lambda: remove_One_Entry(self))
        rm_one_button.grid(row=0, column=3, padx=10, pady=20)

        rm_all_button = Button(button_frame, text="Supprimer tout", command=lambda: remove_all_Records(self))
        rm_all_button.grid(row=0, column=4, padx=10, pady=20)

        clear_button = Button(button_frame, text="Clear", command=lambda: clear_Entries(self))
        clear_button.grid(row=0, column=5, padx=10, pady=20)

        quit_button = Button(button_frame, text="Quitter", command=lambda: quitTourWindow(self))
        quit_button.grid(row=0, column=7, padx=10, pady=20)

        player_button = Button(tourFrame, text="Gestion joueurs",
                                   command=lambda: self.display_playerWindow(self.playerFrame))
        player_button.pack(padx=10, pady=20)

        # Bind the treeview
        #tree_frame.bind("<ButtonRelease-1>", lambda e: selectEntry(self))

        # Bind the players Set
        tree_frame.bind('<Double-Button-1>', lambda event: tour_db_click(self))


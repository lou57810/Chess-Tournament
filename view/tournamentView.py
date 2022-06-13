from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tinydb import TinyDB, Query, where
from tkinter import messagebox
from tkinter.messagebox import *
from control.tournamentController import TournamentController
from control.menuController import MenuController
from view.playerView import PlayerView
from model.tournament import Tournament


class TournamentView:
    def __init__(self, root):
        self.root = root
        self.tree_frame = None
        self.t_frame = None
        self.TOURNAMENT_FIELDS = (
            "Nom du tournoi", "Lieu", "Date debut", "Date fin", "Nombre tours", "Timing", "Description")

        self.tournament_controller = TournamentController(self.root)
        self.menu_controller = MenuController

    def display_tournament_window(self):
        # Create a Treeview Frame
        self.t_frame = Frame(self.root)
        self.t_frame.pack(pady=20)
        self.tree_frame = ttk.Treeview(self.t_frame)

        # ===========================Style & frames=============================
        style = ttk.Style()        # Pick a theme
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
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Configure the Scrollbar
        self.tree_frame = ttk.Treeview(self.t_frame, yscrollcommand=tree_scroll.set, select="extended")
        self.tree_frame.pack()
        tree_scroll.config(command=self.tree_frame.yview)

        # Define Columns
        self.tree_frame["columns"] = self.TOURNAMENT_FIELDS
        self.tree_frame.column('#0', width=0, stretch=NO)
        self.tree_frame.heading('#0', text='', anchor=CENTER)

        for element in self.TOURNAMENT_FIELDS:
            self.tree_frame.column(element, anchor=CENTER, width=120)
            self.tree_frame.heading(element, text=element, anchor=CENTER)

        count = 0
        # Alternative rows
        self.tree_frame.tag_configure('oddrow', background="white")
        self.tree_frame.tag_configure('evenrow', background="lightblue")

        # Display datas
        self.all_tournaments_data = self.tournament_controller.read_data()
        for tournament in self.all_tournaments_data:
            tournament_attributes = []
            for values in vars(tournament).values():
                tournament_attributes.append(values)

            if count % 2 == 0:
                self.tree_frame.insert('', 'end', tournament_attributes[6], text='', values=tournament_attributes,  #tournament_attributes[5]
                                        tags='evenrow')

            else:
                self.tree_frame.insert('', 'end', tournament_attributes[6], text='', values=tournament_attributes, #tournament_attributes[5]
                                        tags='oddrow')
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
            current_elt = StringVar()
            current_elt.set(element)    # Création d'un set

            # Create label
            element_label = Label(self.t_frame, text=element)
            element_label.grid(row=0, column=y)

            if element == "Timing":
                speed_frame = Frame(self.t_frame)
                speed_var = StringVar()
                speed_var.set("None")

                bulletRadio = Radiobutton(speed_frame, anchor=W, text="Bullet", variable=speed_var, value="bullet", width=4)
                fastRadio = Radiobutton(speed_frame, anchor=W,text="Rapide", variable=speed_var, value="rapide", width=5)
                blitzRadio = Radiobutton(speed_frame, anchor=W,text="Blitz", variable=speed_var, value="blitz", width=3)
                bulletRadio.pack(anchor=W, side=LEFT,padx=0)
                fastRadio.pack(anchor=W, side=LEFT,padx=0)
                blitzRadio.pack(anchor=W, side=LEFT,padx=0)
                speed_frame.grid(row=2, column=5)
                input_list.append(speed_var)

            elif element == "Date debut":
                start_date_box = DateEntry(self.t_frame, width=15, locale='fr_FR', selectmode='day', date_pattern='dd/MM/yyyy')
                start_date_box.delete(0, END)
                start_date_box.grid(row=1, column=2, padx=1, pady=10)
                input_list.append(start_date_box)


            elif element == 'Date fin':
                end_date_box = DateEntry(self.t_frame, width=15, locale='fr_FR', selectmode='day', date_pattern='dd/MM/yyyy')
                end_date_box.delete(0, END)
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
                count_spinBox = Spinbox(self.t_frame, from_=0, to=100, font=("helvetica", 10), width=0)
                count_spinBox.grid(row=1, column=4, padx=0, pady=10)
                input_list.append(count_spinBox)

            elif element == "Description":
                descript_box = Entry(self.t_frame, width=20)
                descript_box.grid(row=1, column=6, padx=10, pady=10)
                input_list.append(descript_box)

            y += 1

        # Button for send input to wrapper
        add_tournament_button = Button(self.t_frame, text="Ajouter un tournoi",
                                       command=lambda: self.tournament_controller.add_tournament_button_action(
                                           input_list, self.t_frame, y, add_tournament_button))
        add_tournament_button.grid(row=4, column=0, padx=20,pady=20)

        quit_button = Button(self.t_frame, text="Quitter",
                             command=lambda: TournamentController.quit_tournament_window(self))  # self.quitPlayerView())
        quit_button.grid(row=4, column=6, padx=10, pady=20)

        # Bind the players Set
        self.tree_frame.bind('<Double-Button-1>', lambda event: self.tour_db_click())

    def tour_db_click(self):
        tournament_selected = self.tree_frame.focus()
        temp = self.tree_frame.item(tournament_selected, 'values')
        TournamentController.display_add_player_window(self,temp[0])   # TournamentController récupère le nom du tournoi





            


    """




        # Logical Entry boxes
        nameBox = Entry(data_frame, width=25)
        nameBox.grid(row=1, column=1, padx=10, pady=10)
        input_list.append(nameBox)
        placeBox = Entry(data_frame, width=15)
        placeBox.grid(row=1, column=2, padx=10, pady=10)
        input_list.append(placeBox)
        startDateBox = DateEntry(data_frame, width=15)
        startDateBox.delete(0, END)
        input_list.append(startDateBox)
        startDateBox.grid(row=1, column=3, padx=1, pady=10)
        endDateBox = DateEntry(data_frame, width=15)
        endDateBox.delete(0, END)
        input_list.append(endDateBox)
        endDateBox.grid(row=1, column=4, padx=1, pady=10)
        count_spinBox = Spinbox(data_frame, from_=0, to=100, font=("helvetica", 10), width=2)
        count_spinBox.grid(row=1, column=5, padx=5, pady=10)
        input_list.append(count_spinBox)
        descriptBox = Entry(data_frame, width=25)
        descriptBox.grid(row=1, column=6, padx=10, pady=10)
        input_list.append(descriptBox)

        # RadioButtons
        time_var = StringVar()
        time_var.set(None)
        
        radio_frame = LabelFrame(self.frame, text="Choix du temps")

        bulletRadio = Radiobutton(radio_frame, text="Bullet", variable=time_var, value="bullet", width=10)
        fastRadio = Radiobutton(radio_frame, text="Rapide", variable=time_var, value="rapide", width=10)
        blitzRadio = Radiobutton(radio_frame, text="Blitz", variable=time_var, value="blitz", width=10)
        bulletRadio.grid(row=1, column=0, padx=30)
        fastRadio.grid(row=1, column=1, padx=30)
        blitzRadio.grid(row=1, column=2, padx=30)
        radio_frame.pack(pady=10)
        input_list.append(time_var)
        
        # ================Button Commands(rm = remove)======================

        frame2 = Frame(self.frame)
        frame2.pack(pady=10)

        button_frame = LabelFrame(frame2, text="Commandes")
        button_frame.pack(pady=10)

        add_tournament_button = Button(button_frame, text="Ajouter un tournoi", command=
        lambda: self.tournament_controller.add_tournament_button_action(
            input_list, frame2))
        add_tournament_button.grid(row=0, column=0, padx=10, pady=20)

        display_button = Button(button_frame, text="Afficher les tournois",
                                command=lambda: self.tournament_controller.query_tournament_db(self.tree_frame))
        display_button.grid(row=0, column=1, padx=10, pady=20)

        modif_button = Button(button_frame, text="Modifier", command=lambda: update_one_record(self))
        modif_button.grid(row=0, column=2, padx=10, pady=20)

        rm_one_button = Button(button_frame, text="Test", command=lambda: remove_One_Entry(self))
        rm_one_button.grid(row=0, column=3, padx=10, pady=20)

        rm_all_button = Button(button_frame, text="Supprimer tout", command=lambda: remove_all_Records(self))
        rm_all_button.grid(row=0, column=4, padx=10, pady=20)

        clear_button = Button(button_frame, text="Clear", command=lambda: clear_Entries(self))
        clear_button.grid(row=0, column=5, padx=10, pady=20)

        player_button = Button(button_frame,
                               text="Gestion joueurs", command=lambda: TournamentController.tour_db_click(self))
        player_button.grid(row=0, column=6, padx=10, pady=20)

        quit_button = Button(button_frame, text="Quitter",
                             command=lambda: TournamentController.quit_tournament_window(self))
        quit_button.grid(row=0, column=7, padx=10, pady=20)

        # Bind the treeview
        # tree_frame.bind("<ButtonRelease-1>", lambda e: selectEntry(self))

        # Bind the players Set
        self.tree_frame.bind('<Double-Button-1>', lambda event: TournamentController.tour_db_click(self))

        # ============================Fcts===============================

    """

    """
    def add_entries(self):


        #self.clear_Entries()
        global count
        #tournament_data_list = list()
        # Create Striped Row Tags
        self.tree_frame.tag_configure('oddrow', background="white")
        self.tree_frame.tag_configure('evenrow', background="lightblue")

        # Output to entry boxes
        count = len(self.tree_frame.get_children())

        #self.tree_frame.insert(parent="", index="0",values=())
        if count % 2 == 0:
            self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
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
            self.tree_frame.insert(parent="", index="end", iid=count, text="", values=(
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
        self.clear_Entries(nameBox,placeBox,startDateBox,endDateBox,count_spinBox,time_shot,descriptBox)
        

        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')

        serialized_tournament = {
            'tourn_name': self.nameBox.get(),
            'place_name': self.placeBox.get(),
            'start_date': self.startDateBox.get(),
            'end_date': self.endDateBox.get(),
            'tourns_number': self.count_spinBox.get(),
            'timing': self.time_shot.get(),
            'description': self.descriptBox.get()
        }
    

        tournaments_table.insert(serialized_tournament)
        # values = tree_frame.item(0, 'values')     Retourne un tuple de valeurs de la ligne
        self.clear_Entries()
   

    def query_tournament_db(self):
        global count
        count = 0
        self.tree_frame.tag_configure('oddrow', background="#ecdab9")
        self.tree_frame.tag_configure('evenrow', background="#a47053")

        # tournaments_table = Tournaments.set_tinyDB_Tournaments(self)
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        serialized_tournaments = tournaments_table.all()

        n = 0
        for record in serialized_tournaments:
            if n % 2 == 0:
                self.tree_frame.insert(parent="", index=n, iid=n, text='',
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
                self.tree_frame.insert(parent="", index=n, iid=n, text='',
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
        selected = self.tree_frame.focus()
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
        self.tree_frame.delete(selected)
        if count % 2 == 0:
            self.tree_frame.insert(parent="", index=selected, iid=selected, text="", values=(
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
            self.tree_frame.insert(parent="", index=selected, iid=selected, text="", values=(
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
        x = self.tree_frame.selection()[0]
        self.tree_frame.delete(x)

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
            for record in self.tree_frame.get_children():
                self.tree_frame.delete(record)
            tournaments_table.truncate()

    def clear_Entries(self,nameBox,placeBox,startDateBox,endDateBox,count_spinBox,time_shot,descriptBox):
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
        selected = self.tree_frame.focus()

        # Grab record values
        values = self.tree_frame.item(selected, 'values')
        self.nameBox.insert(0, values[0])
        self.placeBox.insert(0, values[1])
        self.startDateBox.insert(0, values[2])
        self.endDateBox.insert(0, values[3])
        self.count_spinBox.insert(0, values[4])

        # ==========RadioBtn===========
        if values[5] == "bullet":
            self.bulletRadio.invoke()
        elif values[5] == "blitz":
            self.blitzRadio.invoke()
        elif values[5] == "rapide":
            self.fastRadio.invoke()
        # =============================

        self.descriptBox.insert(0, values[6])
    """
    


    """

    def clean_menu_window(self,root):
        for widget in root.winfo_children():
            widget.destroy()
        from view.mainMenu import MainMenu
        menu = MainMenu(self.root)
        menu.display_menu_window()
    """

    """

    for element in self.TOURNAMENT_FIELDS:
        attributes_player.append(player.get(element))
        print("att :",attributes_player)

    for element in self.TOURNAMENT_FIELDS:
        attributes_player.append(player.get(element))
        #print("att :",attributes_player)

    if count % 2 == 0:
        self.tree_frame.insert('', 'end', tournament.get('id'), text='', values=tournament_attributes,
                               tag='evenrow')
    else:
        self.tree_frame.insert('', 'end', tournament.get('id'), text='', values=tournament_attributes,
                               tag='oddrow')
    count += 1

    if count % 2 == 0:
        self.tree_frame.insert('', 'end', tournament_attributes[8], text='', values=tournament_attributes,
                               tag='evenrow')
    else:
        self.tree_frame.insert('', 'end', tournament_attributes[8], text='', values=tournament_attributes,
                               tag='oddrow')
    """

    # self.data_treeview.bind('<Double-Button-1>', self.on_double_click)


from datetime import datetime
from model.player import Player
from model.dbInterface import Interface
from tinydb import TinyDB, where
import tkinter as tk


class PlayerController:
    def __init__(self, root):
        self.root = root
        self.model_interface = Interface()
        self.start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def set_db_tournaments_env(self):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        return tournaments_table

    def set_db_players_env(self):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        return players_table

    def add_player_tree_frame(self, input_list, frame, tree_frame,
                              y, tournament_name, add_player_button,
                              data_fields):
        data = list()
        data.append(tournament_name)
        data_check = True
        count = len(tree_frame.get_children())  # Don't move from here

        for element in input_list:
            data.append(element.get())
            print("data0:", data)
            if not element.get():
                data_check = False
        if data_check:
            data.append('0.0')  # score
            data.append(count + 1)
            player = Player(data)
            player.serialize_player()
            player.write_data()

        tree_frame.tag_configure('oddrow', background="white")
        tree_frame.tag_configure('evenrow', background="lightblue")

        print("count:", count)
        if count % 2 == 0:
            tree_frame.insert('', 'end', text='', values=data, tags='evenrow')
        else:
            tree_frame.insert('', 'end', text='', values=data, tags='oddrow')
        count += 1

        print("data:", data)

    def modify_one_record(self, tree_frame, f_name_box, l_name_box, date_box, gender_var,
                          radiobutton1, radiobutton2, class_spin_box, tournament_name):

        players_table = self.model_interface.set_db_players_env()
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
        players_table.update({'first_name': f_name_box.get()}, where('first_name') == name)
        players_table.update({'last_name': l_name_box.get()}, where('first_name') == name)
        players_table.update({'birth_date': date_box.get()}, where('first_name') == name)
        players_table.update({'gender': gender_var.get()}, where('first_name') == name)
        players_table.update({'rank': class_spin_box.get()}, where('first_name') == name)
        players_table.update({'score': 0}, where('first_name') == name)

    def clear_entries(self, f_name_box, l_name_box, date_box, gender_var, radiobutton1, radiobutton2, class_spin_box):

        f_name_box.delete(0, tk.END)
        l_name_box.delete(0, tk.END)
        date_box.delete(0, tk.END)
        gender_var.set(None)
        class_spin_box.delete(0, tk.END)

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

    def delete_one_player_button(self, tree_frame):
        player_selected = tree_frame.focus()
        # tournament_selected = n° ligne, value = valeurs colonnes
        temp = tree_frame.item(player_selected, 'values')

        for element in tree_frame.selection():
            tree_frame.delete(player_selected)
            Player.delete_player_data(temp[1])  # nom du joueur

    def delete_all_players_button(self, tree_frame):
        tournament_name = tree_frame.item('I002', 'values')[0]

        for values in tree_frame.get_children():
            tree_frame.delete(values)

        players_table = self.model_interface.set_db_players_env()
        players_table.remove(where('tournament_name') == tournament_name)

    def quit_player_window(self):
        self.p_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()
    """
    def display_tournament_round_window(self, tournament_name):
        # ========== Nouvelle fenêtre============================
        from view.mainMenu import MainMenu   # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)

        from view.roundView import RoundView
        self.round_window = RoundView(self.root)
    """

    def quitPlayerWindow(self):
        self.frame.destroy()

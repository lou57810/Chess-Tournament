from tinydb import TinyDB, where
# import tkinter as tk
import time
# from tkinter import ttk
from tkinter import Frame
from model.round import Round
# import operator
# from operator import itemgetter
from datetime import datetime


class RoundController:

    def __init__(self, root):
        self.root = root
        self.round_list = list()
        self.round_players_list = list()
        self.temp_round_players_list = list()
        self.full_pair_players_list = list()
        self.pair_players_id_list = list()
        self.round_number = None
        self.match_list = list()
        self.match = tuple()
        self.round_model = Round()
        self.final_round = list()
        self.start_date = None

    def get_time(self):
        date = time.strftime('%d/%m/%y %H:%M:%S', time.localtime())
        return date

    def set_db_players_env(self):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        return players_table

    def set_db_tournament_players_env(self, tournament_name):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        tournament_players_table = players_table.search(where(
            'tournament_name') == self.tournament_name)
        return tournament_players_table

    def set_db_tournaments_env(self):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        return tournaments_table

    def switch_window(self, tournament_name):
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        """
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
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.tree_frame = ttk.Treeview(
            self.r_frame, yscrollcommand=tree_scroll.set, select="extended")
        self.tree_frame.pack(pady=20)

        self.tree_frame["columns"] = self.HEADING_ROUND_FIELDS
        self.tree_frame.column('#0', width=0, stretch=NO)
        self.tree_frame.heading('#0', text='', anchor=CENTER)

        # Create Striped Row Tags
        self.tree_frame.tag_configure('oddrow', background="#ecdab9")
        self.tree_frame.tag_configure('evenrow', background="#a47053")

        for elt in self.HEADING_ROUND_FIELDS:
            self.tree_frame.column(elt, anchor=CENTER, width=95)
            self.tree_frame.heading(elt, text=elt, anchor=CENTER)
    """

    def gen_rounds(self, tournament_name, tree_frame):
        self.tree_frame = tree_frame
        self.rd_frame = Frame(self.root)
        self.rd_frame.pack()

        self.start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # self.start_date = self.get_time()
        self.set_start_date(self.start_date)

        if len(self.tree_frame.get_children()) == 0:
            round_number = 1

        else:
            # Get n° of round_number
            last_in_tree_frame = len(self.tree_frame.get_children()) - 1
            round_name = str(self.tree_frame.set(last_in_tree_frame, '#2'))
            round_number = int(round_name[5]) + 1

        tree_round_list = self.init_rounds(
            tournament_name, round_number)
        print("round:", round_number)

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

    # ========== Reg players datas in db ============
    def reg_players_values(self, tree_frame, selected):
        players_table = self.set_db_players_env()

        # === Get row rank & score values converted from str to float ===
        elt = int(selected) - 3

        while elt <= int(selected):
            previous_score1 = players_table.search(
                where('first_name') == tree_frame.set(
                    (int(elt)), '#4'))[0]["score"]
            previous_score2 = players_table.search(
                where('first_name') == tree_frame.set(
                    (int(elt)), '#9'))[0]["score"]

            score1 = float(tree_frame.set((int(elt)), '#7'))
            score2 = float(tree_frame.set((int(elt)), '#12'))

            sum1 = float(previous_score1) + score1
            sum2 = float(previous_score2) + score2

            tree_frame.set(elt, '#8', float(sum1))  # (#4 = 'scores_class1')
            tree_frame.set(elt, '#13', float(sum2))

            players_table.update(
                {'score': float(sum1)},
                where('first_name') == tree_frame.set(elt, '#4'))
            players_table.update(
                {'score': float(sum2)},
                where('first_name') == tree_frame.set(elt, '#9'))  # Joueur2
            elt += 1

    def reg_round_matches(self, tree_frame, selected):
        round_list = []
        elt = int(selected) - 3
        while elt <= int(selected):
            match_list1 = list()
            match_list2 = list()
            # Nom Prénom
            match_list1.append(
                tree_frame.set(
                    elt, '#4') + ' ' + tree_frame.set(int(elt), '#5'))
            match_list1.append(tree_frame.set(elt, '#7'))  # Score

            match_list2.append(
                tree_frame.set(
                    elt, '#9') + ' ' + tree_frame.set(int(elt), '#10'))
            match_list2.append(tree_frame.set(elt, '#12'))

            match = (match_list1, match_list2)
            round_list.append(match)
            elt += 1

        return round_list

    def insert_round_datas(self, round_list, round_number, start_date):
        round_list.insert(0, round_number)
        round_list.insert(1, start_date)
        round_list.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.round_model.all_tournament_rounds_list.append(round_list)

    def valid_round(self, tree_frame, tournament_name):
        self.start_date = self.get_start_date()
        print("start_date:", self.start_date)
        tournaments_table = self.set_db_tournaments_env()
        round_list = list()
        selected = tree_frame.focus()
        round_name = tree_frame.set(int(selected), '#2')

        if round_name == 'Round1':
            self.reg_players_values(tree_frame, selected)
            round_list = self.reg_round_matches(
                tree_frame, selected)

            if int(selected) == 3:
                self.insert_round_datas(round_list, round_name, self.start_date)

        elif round_name == 'Round2':
            self.reg_players_values(tree_frame, selected)
            round_list = self.reg_round_matches(
                tree_frame, selected)

            if int(selected) == 7:
                self.insert_round_datas(round_list, round_name, self.start_date)

        elif round_name == 'Round3':
            self.reg_players_values(tree_frame, selected)
            round_list = self.reg_round_matches(
                tree_frame, selected)
            if int(selected) == 11:
                self.insert_round_datas(round_list, round_name, self.start_date)

        elif round_name == 'Round4':
            self.reg_players_values(tree_frame, selected)
            round_list = self.reg_round_matches(
                tree_frame, selected)
            if int(selected) == 15:
                self.insert_round_datas(round_list, round_name, self.start_date)

            tournaments_table.update(
                {'rounds_lists': self.round_model.all_tournament_rounds_list},
                where('tournament_name') == tournament_name)

    def match_data(self):
        self.round_model.players_list = self.round_model.create_players_list()
        self.sort_players()
        self.create_upper_and_lower_list()
        return self.create_match()

    """
    def sort_players(self):
        # Sort players by ranking
        self.round_model.players_list.sort(
        key=lambda x: x.ranking, reverse=True)
        # print(self.round_model.players_list)
    """

    def sort_matches(self, round_number, one_round_players_list):

        if round_number == 1:
            one_round_players_list.sort(
                key=lambda x: x[3], reverse=True)  # Tri  rang
        else:
            one_round_players_list.sort(
                key=lambda x: (x[5], x[3]), reverse=True)  # Tri score et rang

    def create_upper_and_lower_list(self):
        length = len(self.round_model.players_list)
        i = 0
        while i < length:
            if i < length / 2:
                self.round_model.upper_list.append(
                    self.round_model.players_list[i])
            else:
                self.round_model.lower_list.append(
                    self.round_model.players_list[i])
            i += 1

    """
    def create_match(self):
        length = len(self.round_model.players_list)
        i = 0
        while i < length / 2:
            list_1 = [self.round_model.lower_list[i].id, 0]
            list_2 = [self.round_model.upper_list[i].id, 0]
            match = (list_1, list_2)
            self.round_model.matches_list.append(match)
            i += 1
        return self.round_model.matches_list
    """

    def quit_round_window(self):
        self.rd_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()

    def reverse_pair(self, pair):
        new_pair = pair[::-1]
        return new_pair

    def create_pairs(self, one_round_players_list):
        id_list = list()
        upper_id = list()
        lower_id = list()
        i = 0
        while i < len(one_round_players_list):
            if i % 2 == 0:
                upper_id.append(one_round_players_list[i][6])
            else:
                lower_id.append(one_round_players_list[i][6])
            i += 1

        for elt in zip(upper_id, lower_id):
            id_list.append(elt)

        return id_list

    def init_players_list(self, tournament_name, round_number):
        one_round_players_list = list()
        self.tournament_name = tournament_name
        players_table = self.set_db_players_env()
        serialized_players = []
        serialized_players = players_table.search(
            where('tournament_name') == self.tournament_name)
        pair_players_id_list = list()

        # Liste dictionnaires comprenant:
        # tournoi, nom, prénom,date, rang, score, id
        i = 0
        while i < len(serialized_players):
            # i --> 4 (matches)
            init_list = [
                serialized_players[i].get('tournament_name'),
                serialized_players[i].get('first_name'),
                serialized_players[i].get('last_name'),
                int(serialized_players[i].get('rank')),
                0.0,  # score début de match
                float(serialized_players[i].get('score')),
                serialized_players[i].get('id')
            ]
            # ex: init_list:
            # ['Europa Chess', 'Flamand', 'Julia', 310, 0.0, 0.0, 8]... x 8
            one_round_players_list.append(init_list)

            i += 1
        # ========================= Tri rangs et scores ====================
        self.sort_matches(round_number, one_round_players_list)
        # ========================== Create pairs ==========================
        pair_players_id_list = self.create_pairs(one_round_players_list)

        # return (one_round_players_list, pair_players_id_list)
        return pair_players_id_list

    def final_init_list(self, tournament_name, pair_players_id_list):
        players_list = list()
        for elt in pair_players_id_list:
            players_list.append(
                self.display_id_values(elt[0], tournament_name))
            players_list.append(
                self.display_id_values(elt[1], tournament_name))
        return players_list

    def display_id_values(self, player_id, tournament_name):
        players_table = self.set_db_tournament_players_env(tournament_name)
        init_player = list()
        for elt in players_table:
            if elt['id'] == player_id:
                # i --> 4 (matches)
                init_player = [
                    elt['tournament_name'],
                    elt['first_name'],
                    elt['last_name'],
                    elt['rank'],
                    0.0,  # score début de match
                    elt['score'],
                    elt['id']
                ]
        return init_player

    # Initialisation rounds
    def init_rounds(self, tournament_name, round_number):
        pair_players_id_list = list()
        compare_list = list()
        pair_players_id_list = self.init_players_list(tournament_name, round_number)

        # convert tuples in list because tuples are immuables:
        # utilisation de liste de compréhension
        pair_players_id_list = [list(i) for i in pair_players_id_list]
        print("pair_players_id_list_origin:", pair_players_id_list)
        # =============== INSERTION ===============
        for elt in pair_players_id_list:
            self.full_pair_players_list.append(elt)  # cumul liste  pairs

        # ========== Compare list = total list - current list ========
        for elt in self.full_pair_players_list:
            compare_list.append(elt)
        i = 0
        while i < 4:  # Sub current list
            compare_list.pop()
            i += 1
        # ========================== Occurrences ============================
        print("compare_list:", compare_list)
        full_compare_list = self.reverse_compare_id_list(compare_list)

        self.switch_id_list(full_compare_list, pair_players_id_list)
        print("pair_players_id_list_final:", pair_players_id_list)

        final_round_list = self.final_init_list(
            tournament_name, pair_players_id_list)
        print("final_roundAffiche:", final_round_list)
        return final_round_list

    # Translation x till no doubles
    def switch_id_list(self, full_compare_list, pair_players_id_list):
        i = 0
        data_check = False
        if len(full_compare_list) != 0:
            while i < len(full_compare_list):
                for elt in pair_players_id_list:
                    if elt == full_compare_list[i]:
                        print("doublon:", elt)
                        pair_players_id_list = self.pairs_id_translate(
                            elt, pair_players_id_list)
                        data_check == True

                i += 1
        if data_check == True:
            self.switch_id_list(full_compare_list, pair_players_id_list)
        elif len(full_compare_list) != 0:
            while i < len(full_compare_list):
                for elt in pair_players_id_list:
                    if elt != full_compare_list[i]:
                        pass
        return pair_players_id_list

    def pairs_id_translate(self, elt, pair_players_id_list):
        temp = pair_players_id_list[0][0]  # pair_id[0]
        j = 0
        while j < len(pair_players_id_list) - 1:
            pair_players_id_list[j][0] = pair_players_id_list[j + 1][0]
            j += 1
            pair_players_id_list[j][0] = temp
        return pair_players_id_list

    def reverse_compare_id_list(self, compare_list):
        sum = list()
        for elt1 in compare_list:  # ronde actuelle
            sum.append(self.reverse_pair(elt1))
        for elt2 in sum:
            compare_list.append(elt2)
        return compare_list

        # =========================== Button fct ================================

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

    def set_start_date(self, start_date):
        # print("s_d:", start_date)
        return start_date

    def get_start_date(self):
        self.start_date = self.set_start_date(self.start_date)
        return self.start_date

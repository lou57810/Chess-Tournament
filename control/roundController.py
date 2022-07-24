import time
# from tkinter import Frame
from tinydb import where
from model.round import Round
from model.dbInterface import Interface
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
        self.model_interface = Interface()
        self.final_round = list()
        self.start_date = None

    def get_time(self):
        date = time.strftime('%d/%m/%y %H:%M:%S', time.localtime())
        return date

    def switch_window(self, tournament_name):
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
    """
    def gen_round(self, tournament_name, tree_frame):
        self.tree_frame = tree_frame
        self.rd_frame = Frame(self.root)
        self.rd_frame.pack()
        self.start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.set_start_date(self.start_date)
        if len(self.tree_frame.get_children()) == 0:
            round_number = 1
        else:
            # Get next n° of round_number
            last_in_tree_frame = len(self.tree_frame.get_children()) - 1
            round_name = str(self.tree_frame.set(last_in_tree_frame, '#2'))
            round_number = int(round_name[5]) + 1
    def create_upper_and_lower_list(self, tournament_name):
        # Read all players data
        tournaments_table = self.model_interface.set_db_players_env()
        self.round_model.players_list = tournaments_table.search(where('first_name') == tournament_name)
        print("rmpl:", self.round_model.players_list)
        # Split players in two list
        length = len(self.round_model.players_list)
        i = 0
        while i < length:
            if i < length / 2:
                self.round_model.upper_list.append(self.round_model.players_list[i])
            else:
                self.round_model.lower_list.append(self.round_model.players_list[i])
            i += 1
        print("up & Low:", self.round_model.upper_list, self.round_model.lower_list)
    """
    # ========== Reg players datas in db ============
    def reg_players_values(self, tree_frame, selected):
        players_table = self.model_interface.set_db_players_env()

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
            match_list1.append(tree_frame.set(elt, '#4') + ' ' + tree_frame.set(int(elt), '#5'))
            match_list1.append(tree_frame.set(elt, '#7'))  # Score

            match_list2.append(tree_frame.set(elt, '#9') + ' ' + tree_frame.set(int(elt), '#10'))
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

        tournaments_table = self.model_interface.set_db_tournaments_env()
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

    def quit_round_window(self):
        self.rd_frame.destroy()
        from view.mainMenu import MainMenu  # Outside déclaration
        main_menu = MainMenu(self.root)
        main_menu.clean_menu_window(self.root)
        main_menu.display_menu_window()

    def reverse_pair(self, pair):
        new_pair = pair[::-1]
        return new_pair

    def final_init_list(self, tournament_name, pair_players_id_list):
        players_list = list()
        for elt in pair_players_id_list:
            players_list.append(
                self.display_id_values(elt[0], tournament_name))
            players_list.append(
                self.display_id_values(elt[1], tournament_name))
        return players_list

    def display_id_values(self, player_id, tournament_name):
        players_table = self.model_interface.set_db_players_env()
        tournament_players_table = players_table.search(where(
            'tournament_name') == tournament_name)
        init_player = list()
        for elt in tournament_players_table:
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
        # print("init_player:", init_player)
        return init_player

    # Initialisation rounds
    def init_rounds(self, tournament_name, round_number):
        pair_players_id_list = list()
        compare_list = list()
        pair_players_id_list = self.round_model.init_sorted_round_players_id_list(tournament_name, round_number)
        print("Liste courante:", pair_players_id_list)

        # liste de compréhension: convert tuples in list because tuples are immuables:
        pair_players_id_list = [list(i) for i in pair_players_id_list]
        # =============== INSERTION ===============
        for elt in pair_players_id_list:
            self.full_pair_players_list.append(elt)  # cumul liste  paires à chaques rondes

        # ========== Compare list = total list - current list ========
        for elt in self.full_pair_players_list:
            compare_list.append(elt)
        i = 0
        while i < 4:  # Sub current list
            compare_list.pop()
            i += 1
        # ========================== Occurrences ============================
        full_compare_list = self.reverse_compare_id_list(compare_list)
        print("Liste de tous les derniers Matchs:", full_compare_list)
        # compare er echange les joueurs
        pair_players_id_list = self.switch_id_list(full_compare_list, pair_players_id_list)
        print("Liste après tri doublons:", pair_players_id_list)
        # Liste des joueurs après comparaison des doublons
        final_round_list = self.final_init_list(
            tournament_name, pair_players_id_list)
        return final_round_list

    # Translation x till no doubles
    def switch_id_list(self, full_compare_list, pair_players_id_list):
        i = 0
        data_check = False
        if len(full_compare_list) != 0:
            while i < len(full_compare_list):
                for elt in pair_players_id_list:
                    if elt == full_compare_list[i]:
                        print("doublon1:", elt)
                        pair_players_id_list = self.pairs_id_translate(
                            elt, pair_players_id_list)
                        data_check = True
                    else:
                        data_check = False
                i += 1
        if data_check:
            self.switch_id_list(full_compare_list, pair_players_id_list)
        else:
            return pair_players_id_list

    def pairs_id_translate(self, elt, pair_players_id_list):
        temp = pair_players_id_list[0][0]  # pair_id[0]
        j = 0
        while j < len(pair_players_id_list) - 1:
            pair_players_id_list[j][0] = pair_players_id_list[j + 1][0]
            j += 1
            pair_players_id_list[j][0] = temp
        return pair_players_id_list

    # Add list & reverse list
    def reverse_compare_id_list(self, compare_list):
        sum = list()
        for elt1 in compare_list:  # ronde actuelle
            sum.append(self.reverse_pair(elt1))
        for elt2 in sum:
            compare_list.append(elt2)
        return compare_list

    def set_start_date(self, start_date):
        # print("s_d:", start_date)
        return start_date

    def get_start_date(self):
        self.start_date = self.set_start_date(self.start_date)
        return self.start_date

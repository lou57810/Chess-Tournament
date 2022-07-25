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

    def insert_round_datas(self, round_list, round_number, start_date):
        round_list.insert(0, round_number)
        round_list.insert(1, start_date)
        round_list.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.round_model.all_tournament_rounds_list.append(round_list)

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

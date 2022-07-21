from tinydb import where
# from model.player import Player
from model.dbInterface import Interface


class Round:

    def __init__(self, *args):

        self.players_list = []
        self.upper_list = []
        self.lower_list = []
        self.round_list = list()
        self.all_tournament_rounds_list = []
        self.serialized_round_data = {}
        self.model_interface = Interface()
        self.DATA_FIELDS = (
            'Nom', 'Prénom',
            'Date de naissance',
            'Genre', 'Classement')

        for element in args:
            self.name = element[0]
            self.start_time = element[1]
            self.matches_list = element[2]
            self.end_time = element[3]

    def serialize_round_data(self):
        self.serialized_round_data = {'name': self.name,
                                      'start_time': self.start_time,
                                      'matches': self.matches_list,
                                      'end_time': self.end_time,
                                      }
        return self.serialized_round_data

    """
    def create_players_list(self):
        # Read all players data
        #all_players_data = Player.read_data()
        all_players_data = self.model_interface.set_db_players_all()
        # print("all_players_data:", all_players_data)
        # Get dictionary values for each players
        for element in all_players_data:
            player_data = []
            i = 0
            for key in self.DATA_FIELDS:
                player_data.append(element.get(key))
                i += 1

            player_data.append(element.get('score'))

            # Create instance for each player
            player = Player(player_data)
            self.players_list.append(player)
        return self.players_list
    """

    def sort_matches(self, one_round_players_list):
        one_round_players_list.sort(
            key=lambda x: (x[5], x[3]), reverse=True)  # Tri score et rang

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

    # ===== Transform dictionnary players_list in list of sorted players_list & get id players_tuples ========

    def init_sorted_round_players_id_list(self, tournament_name, round_number):
        players_table = self.model_interface.set_db_players_env()
        serialized_round_players_list = players_table.search(
            where('tournament_name') == tournament_name)

        one_round_players_list = list()
        # List dictionnairies comprenant: tournoi, nom, prénom,date, rang, score, id
        i = 0
        while i < len(serialized_round_players_list):
            # i --> 4 (matches)
            init_list = [
                serialized_round_players_list[i].get('tournament_name'),
                serialized_round_players_list[i].get('first_name'),
                serialized_round_players_list[i].get('last_name'),
                int(serialized_round_players_list[i].get('rank')),
                0.0,  # score début de match
                float(serialized_round_players_list[i].get('score')),
                serialized_round_players_list[i].get('id')
            ]
            # ex: init_list:
            # ['Europa Chess', 'Flamand', 'Julia', 310, 0.0, 0.0, 8]... x 8
            one_round_players_list.append(init_list)
            i += 1

        # ========================= Tri rangs et scores ====================
        self.sort_matches(one_round_players_list)
        # ========================== Create pairs ==========================
        pair_players_id_list = self.create_pairs(one_round_players_list)
        # print("pairs:", pair_players_id_list)
        return pair_players_id_list

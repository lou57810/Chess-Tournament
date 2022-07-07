from tinydb import TinyDB, where
# import data	# db_tournaments.json
from model.player import Player
# from model.tournament import Tournaments
# from tinydb.operations import set
# import copy


class Round:

    def __init__(self, *args):
        # self.PLAYER_FIELDS = (
        # 'tournament_name', 'first_name', 'last_name'
        # 'birth_date', 'gender', 'rank', 'score')
        # self.all_rounds_list = []
        self.players_list = []
        self.upper_list = []
        self.lower_list = []
        self.round_list = list()
        self.all_tournament_rounds_list = []
        self.serialized_round_players = {}
        """
        for element in args:
            self.first_name = element[0]
            self.last_name = element[1]
            self.rank = element[2]
            self.score = element[3]

        for element in args:
            self.round_name = element[0]
            self.round_date1 = element[1]
            self.round_list = element[2]
            self.round_date2 = elemnt[3]
        """

    def serialize_round_players(self):
        self.serialized_round_players = {
                                        'first_name':   self.first_name,
                                        'last_name':    self.last_name,
                                        'rank':         self.rank,
                                        'score':        self.score,
                                        'id':           self.id
                                        }

    def get_round_player_scores(self, data_player_list2):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        i = 0
        while i < len(data_player_list2):
            players_table.update(
                {'score': data_player_list2[i][1]},
                where('id') == data_player_list2[i][0])
            i += 1

    def reg_db_rounds(self):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        tournaments_table.update({'rounds_list': Round.all_rounds})

    def create_players_list(self):
        # Read all players data
        all_players_data = Player.read_data()

        # Get dictionary values for each players
        for element in all_players_data:
            player_data = []
            i = 0
            for key in self.PLAYER_FIELDS:
                player_data.append(element.get(key))
                i += 1

            player_data.append(element.get('score'))

            # Create instance for each player
            player = Player(player_data)
            self.players_list.append(player)
        return self.players_list

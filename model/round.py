from tinydb import TinyDB, Query, where
# import data	# db_tournaments.json
from model.player import Player
# from model.tournament import Tournaments
from tinydb.operations import set
import copy


class Round:
    
    def __init__(self, *args):
        self.players_list = []
        self.upper_list = []
        self.lower_list = []
        self.serialized_round_data = []
        self.matches_list = []
        #self.PLAYER_FIELD = ('Nom', 'Prénom', 'Date de naissance', 'Sexe', 'Classement')

        for element in args:
            self.first_name = element[0]
            self.last_name = element[1]
            #self.start_time = element[2]
            #self.end_time = element[3]
            self.matches_list = element[2]
            self.id = element[3]


    def get_round_list2(self, data2):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        Round.j += 1
        if Round.j <= 4:
            Round.round2.append(data2)
        if Round.j == 4:
            Round.all_rounds.append(Round.round2)
            #tournaments_table.update({'rounds_list': Round.all_rounds})  # Round.all_rounds})
            Round.reg_db_rounds(self)

    def get_round_player_scores(self,data_player_list2):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        #print("date_player_list2:",data_player_list2)
        i = 0
        while i < len(data_player_list2):
            #print("score:",data_player_list2[i][1])
            #print("id:", data_player_list2[i][0])
            players_table.update({'score': data_player_list2[i][1]}, where('id') == data_player_list2[i][0])
            i += 1




    def reg_db_rounds(self):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        tournaments_table.update({'rounds_list': Round.all_rounds})  # Round.all_rounds})

    def create_players_list(self):
        #Read all players data
        all_players_data = Player.read_data()

        # Get dictionary values for each players
        for element in all_players_data:
            player_data = []
            i = 0
            for key in self.FRENCH_NAME_OF_PLAYER_FIELD:
                player_data.append(element.get(key))
                i += 1

            player_data.append(element.get('score'))
            player_data.append(element.get('id'))

            # Create instance for each player
            player = Player(player_data)
            self.players_list.append(player)
        return self.players_list



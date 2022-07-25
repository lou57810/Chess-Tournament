from model.dbInterface import Interface
from tinydb import where


class Player:

    def __init__(self, *args):
        for element in args:
            self.tournament_name = element[0]
            self.first_name = element[1]
            self.last_name = element[2]
            self.birth_date = element[3]
            self.gender = element[4]
            self.rank = element[5]
            self.score = element[6]
            self.id = element[7]

        self.serialized_player = {}
        self.model_interface = Interface()

    def serialize_player(self):
        self.serialized_player = {
            'tournament_name': self.tournament_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'rank': self.rank,
            'score': self.score,
            'id': self.id
        }

    def write_data(self):
        """Write player data in DB"""
        players_table = self.model_interface.set_db_players_env()
        players_table.insert(self.serialized_player)
        return self.serialized_player

    def delete_player_data(self, data):
        players_table = self.model_interface.set_db_players_env()
        players_table.remove(where('first_name') == data)

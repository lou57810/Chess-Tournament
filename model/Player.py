from tinydb import TinyDB, where

class Player:
    def __init__(self, *args):

        for element in args:
            self.tournament_name        = element[0]
            self.first_name             = element[1]
            self.last_name              = element[2]
            self.birth_date             = element[3]
            self.gender                 = element[4]
            self.rank                   = element[5]
            self.score                  = element[6]
            self.id                     = element[7]

        self.serialized_player = {}

    def serialize_player(self):        
        self.serialized_player = {
                                  'tournament_name':        self.tournament_name,
                                  'first_name':             self.first_name,
                                  'last_name':              self.last_name,
                                  'birth_date':             self.birth_date,
                                  'gender':                 self.gender,
                                  'rank':                   self.rank,
                                  'score':                  self.score,
                                  'id':                     self.id
                                  }
    """
    @staticmethod
    def read_data():
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        return players_table.all()
    """

    def write_data(self):
        """Write player data in DB"""
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        players_table.insert(self.serialized_player)
        return self.serialized_player
    """
    def set_tinyDB_Players(self):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        return players_table.all()
    

    def delete_db_data(self):
        db = TinyDB('data/db_tournaments.json')
        db.drop_table('players')

    @staticmethod
    def read_data():
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        return players_table.all()
    """

    @staticmethod
    def delete_player_data(data):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        players_table.remove(where('first_name') == data)

    @staticmethod
    def delete_all_data():
        db = TinyDB('data/db_tournaments.json')
        db.drop_table('players')





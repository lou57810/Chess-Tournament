from tinydb import TinyDB, where

class Player:
    def __init__(self,id,first_name,last_name,birth_date,gender,rank,score):
        self.serialized_player = {}
        self.id         = id
        self.first_name = first_name
        self.last_name  = last_name
        self.birth_date = birth_date
        self.gender     = gender
        self.rank       = rank
        self.score      = score

    def serialize_player(self):        
        self.serialized_player = {'id':         self.id,
                                  'first_name': self.first_name,
                                  'last_name':  self.last_name,
                                  'birth_date': self.birth_date,
                                  'gender':     self.gender,
                                  'rank':       self.rank,
                                  'score':      self.score
                                  }

    def set_tinyDB_Players(self):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        return players_table


     
	

   
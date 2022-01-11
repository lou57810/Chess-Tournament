from tinydb import TinyDB, where

class Player:	
    def __init__(self, first_name,last_name,birth_date,gender,rank):	        
        self.first_name    = first_name
        self.last_name     = last_name
        self.birth_date    = birth_date
        self.gender        = gender
        self.rank          = rank

        self.serialized_player = {'first_name': self.first_name,
                                  'last_name':  self.last_name,
                                  'birth_date': self.birth_date,
                                  'gender':     self.gender,
                                  'rank':       self.rank
                                  }
"""
        
        first_name = serialized_player['first_name']
        last_name  = serialized_player['last_name']
        birth_date = serialized_player['birth_date']
        gender     = serialized_player['gender']
        classement = serialized_player['classement']
"""
     
	

   
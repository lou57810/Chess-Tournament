class Player:	
    def __init__(self, first_name,last_name,birth_date,gender,classement):	        
        self.first_name    = first_name
        self.last_name     = last_name
        self.birth_date    = birth_date
        self.gender        = gender
        self.classement    = classement
	            
    def serialize_player(self):
        self.serialized_player = {'first_name': self.first_name,
                                  'last_name': self.last_name,
                                  'birth_date': self.birth_date,
                                  'gender': self.gender,
                                  'Classement': self.classement
                                }
	

   
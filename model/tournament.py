from tinydb import TinyDB, where

  

class Tournaments:

    def __init__(self,tourn_name,place_name,start_date,end_date,tourns_number,timing,description,rounds_list):
        
        self.tourn_name = tourn_name
        self.place_name = place_name
        self.start_date = start_date
        self.end_date = end_date
        self.tourns_number = tourns_number
        self.timing = timing
        self.description = description
        self.rounds_list = rounds_list

        self.serialized_tournaments = {}

    def fct_serialize_tournaments(self):
        self.serialized_tournaments = {
            'tourn_name': self.tourn_name,
            'place_name': self.place_name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'tourns_number': self.tourns_number,
            'timing': self.timing,
            'description': self.description,
            'rounds_list': self.rounds_list
        }
        return self.serialized_tournaments



    """

    def write_datas(self):
        roundList = []
        roundList = Round.getMatch(r)
        self.serialized_tournaments['player_list'] = self.player_list
        for elt in self.roundList:
            roundList.append(elt.serialized_round_data())
            print("elt: ",elt.serialized_round_data())
        self.serialized_tournaments['rounds_list'] = roundList
        self.serialized_tournaments['id'] = self.id

        self.tournaments_table.insert(self.serialized_tournaments)
        print("Tournoi +: ",self.serialized_tournaments)
    

    def read_data(self):
        set_tinyDB_Tournaments()
        #db = TinyDB('data/tournaments_db.json')
        #tournament_table = db.table('tournaments')
        return tournaments_table.all()
    """

    def tournaments_reg_datas(self,rounds_list):
    #print("sPlayerlids", self.player_list)
        #self.serialized_tournaments['players'] = self.player_list
        rounds_list = []
        for elt in self.rounds_list:
            self.rounds_list.append(elt.serialize_round_data())
        self.serialized_tournaments['rounds_list'] = self.rounds_list
        self.serialized_tournaments['id'] = self.id

        self.tournaments_table.insert(self.serialized_tournaments)
        print(f'Tournoi ajouté :{self.serialized_tournaments}')

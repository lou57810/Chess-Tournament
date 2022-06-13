from tinydb import TinyDB, where


class Tournament:

    def __init__(self, *args):
        for element in args:
            #print("element:",element)
            self.tournament_name    = element[0]
            self.place_name         = element[1]
            self.start_date         = element[2]
            self.end_date           = element[3]
            self.turns_number       = element[4]
            self.timing             = element[5]
            self.description        = element[6]
            self.players_list       = element[7]
            self.rounds_lists        = element[8]
            #self.id                 = element[9]

        self.tournament_table = self.set_tournaments_table()
        self.serialized_tournaments = {}

    def serialize_tournaments(self):
        self.serialized_tournaments = {
                                        'tournament_name':      self.tournament_name,
                                        'place':                self.place_name,
                                        'start_date':           self.start_date,
                                        'end_date':             self.end_date,
                                        'number_turns':         self.turns_number,
                                        'timing':               self.timing,
                                        'description':          self.description,
                                        'rounds_lists':         self.rounds_lists
        }

    def set_tournaments_table(self):
        db = TinyDB('data/db_tournaments.json')
        return db.table('tournaments')

    def write_data(self):
        """Write tournament data in DB"""
        db = TinyDB('data/db_tournaments.json')
        tournament_table = db.table('tournaments')

        # Add players, rounds list and id attributes
        #self.serialized_tournaments['players_list'] = self.players_list
        #rounds_list = []
        #for element in self.rounds_list:
            #rounds_list.append(element.serialize_round_data())
        #self.serialized_tournaments['rounds_list'] = rounds_list
        #i = 1
        #while tournament_table.search(where('id') == i):
            #i += 1
        #self.serialized_tournaments['id'] = i

        tournament_table.insert(self.serialized_tournaments)
        print(f'Tournoi ajouté :{self.serialized_tournaments}')

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
    """

    @staticmethod
    def read_data():
        db = TinyDB('data/db_tournaments.json')
        tournament_table = db.table('tournaments')
        return tournament_table.all()

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
        
    """

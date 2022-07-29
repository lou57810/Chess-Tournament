from model.dbInterface import Interface


class Tournament:

    def __init__(self, *args):
        for element in args:
            self.tournament_name = element[0]
            self.place_name = element[1]
            self.start_date = element[2]
            self.end_date = element[3]
            self.turns_number = element[4]
            self.timing = element[5]
            self.description = element[6]
            self.players_list = element[7]
            self.rounds_lists = element[8]

        self.serialized_tournaments = {}
        self.model_interface = Interface()

    def serialize_tournaments(self):
        self.serialized_tournaments = {
            'tournament_name': self.tournament_name,
            'place': self.place_name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'number_turns': self.turns_number,
            'timing': self.timing,
            'description': self.description,
            'rounds_lists': self.rounds_lists
        }

    def write_data(self):
        # Write tournament data in DB
        tournament_table = self.model_interface.set_db_tournaments_env()
        tournament_table.insert(self.serialized_tournaments)

    # @staticmethod
    def read_data(self):
        tournament_table = self.model_interface.set_db_tournaments_env()
        return tournament_table.all()

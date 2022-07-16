from tinydb import TinyDB


class Interface:
    def __init__(self):
        pass

    def set_db_tournaments_env(self):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        return tournaments_table

    def set_db_players_env(self):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        return players_table

    def set_db_players_all(self):
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')
        serialized_players = players_table.all()
        return serialized_players

    def set_db_tournaments_all(self):
        db = TinyDB('data/db_tournaments.json')
        tournaments_table = db.table('tournaments')
        serialized_tournaments = tournaments_table.all()
        return serialized_tournaments

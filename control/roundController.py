from tinydb import TinyDB, Query, where
import time





class RoundController:

    def __init__(self, root_window):
        self.root_window = root_window
        self.round_model = Round()

    def getTime():
        date = time.strftime('%d/%m/%y %H:%M:%S', time.localtime())
        return date

    def createRound(self):
        round = Round(data)
        round.serialize_rounds()
        return round










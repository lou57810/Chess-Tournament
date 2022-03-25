import tkinter as tk
from tkinter import *
from tkinter import ttk
from view.mainMenu import MainMenu
from tinydb import TinyDB, Query, where
from control.tournamentController import TournamentController


class Controller():
    def __init__(self):
        pass

    def run_tournamentApp(self):
        MainMenu.draw_mainMenuView(self)
        # TournamentController.get_tournament_instance_list(self)

    def getTime(self):
        date = time.strftime('%d/%m/%y %H:%M:%S', time.localtime())
        return date

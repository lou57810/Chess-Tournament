from tkinter import *
from tkinter.messagebox import *
from view.tournamentView import TournamentView
from view.playerView import PlayerView
from view.roundView import RoundView

from control.menuController import MenuController
from control.tournamentController import TournamentController

from tinydb import TinyDB, where


class MainMenu:

    def __init__(self, root):
        self.root = root
        self.player_window = PlayerView(self.root)
        self.tournament_window = TournamentView(self.root)
        self.round_window = RoundView(self.root)

        #self.tournament_controller = TournamentController(self.root)

    def display_menu_window(self):
        menuBar = Menu(self.root)
        menuFile = Menu(menuBar)
        menuEdition = Menu(menuBar)
        menuOutils = Menu(menuBar)
        menuHelp = Menu(menuBar)

        menuBar.add_cascade(label="Fichier", menu=menuFile)
        menuBar.add_cascade(label="Edition", menu=menuEdition)
        menuBar.add_cascade(label="Outils", menu=menuOutils)
        menuBar.add_cascade(label="?", menu=menuHelp)

        # Commands
        menuFile.add_command(label="Gestion Tournoi", command=lambda: MenuController.display_tournament_window(self))
        # menuFile.add_command(label="Gestion joueurs", command=lambda: MenuController.display_player_window(self))
        menuFile.add_command(label="Afficher les resultats")
        menuFile.add_command(label="Enregistrer les résultats")
        menuFile.add_command(label="Modifier les resultats")
        menuFile.add_separator()
        menuFile.add_command(label="Quitter", command=lambda: MenuController.fct_quit(self))

        menuEdition.add_command(label="Edition du rapport")
        menuEdition.add_command(label="Impression du rapport", command=lambda: MenuController.fct_warning(self))
        menuEdition.add_separator()
        menuEdition.add_command(label="Rechercher", command=lambda: MenuController.fct_yes_no(self))

        menuOutils.add_command(label="Parametres")

        menuHelp.add_command(label="Obtenir de l'aide", command=lambda: MenuController.fct_error(self))
        menuHelp.add_command(label="Mise à jour", command=lambda: MenuController.maj_fct(self))
        menuHelp.add_separator()
        menuHelp.add_command(label="A propos", command=lambda: MenuController.show_about(self))

        self.root.config(menu=menuBar)

    def clean_menu_window(self, root):
        for widget in root.winfo_children():
            widget.destroy()
        self.display_menu_window()

    def display_player_window(self):
        self.clean_menu_window(self.root)
        self.display_menu_window()
        self.player_window.call_tournament_player_list(tournament_name)

    def display_tournament_window(self):
        self.clean_menu_window(self.root)
        self.display_menu_window()
        self.tournament_window.display_tournament_window()
        self.tournament_window.tournament_data_set()

    def display_round_window(self):
        self.clean_menu_window(self.root)
        self.display_menu_window()
        





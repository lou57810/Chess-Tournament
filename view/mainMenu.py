# from tkinter import *
# from tkinter.messagebox import *
# from tkinter import Messagebox
from tkinter import Menu
from view.tournamentView import TournamentView
from view.playerView import PlayerView
from view.roundView import RoundView
from control.menuController import MenuController


class MainMenu:

    def __init__(self, root):
        self.root = root
        self.player_window = PlayerView(self.root)
        self.tournament_window = TournamentView(self.root)
        self.round_window = RoundView(self.root)

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
        menuFile.add_command(label="Enregistrer les résultats", command=lambda: MenuController.param_fct(self))
        menuFile.add_command(label="Impression des rapports", command=lambda: MenuController.fct_warning(self))
        menuFile.add_separator()
        menuFile.add_command(label="Quitter",
                             command=lambda: MenuController.fct_quit(self))

        menuEdition.add_command(label="Tous les acteurs alpha")
        menuEdition.add_command(label="Tous les acteurs num")
        menuEdition.add_command(label=" Tous les joueurs alpha")
        menuEdition.add_command(label=" Tous les joueurs num")
        menuEdition.add_command(label=" Tous les Tournois")
        menuEdition.add_command(label=" Tous les Tours d'un Tournoi")
        menuEdition.add_command(label=" Tous les Matchs d'un Tournoi")

        menuEdition.add_separator()
        menuEdition.add_command(
            label="Rechercher",
            command=lambda: MenuController.fct_yes_no(self))

        menuOutils.add_command(label="Parametres",
                               command=lambda: MenuController.param_fct(self))

        menuHelp.add_command(
            label="Obtenir de l'aide",
            command=lambda: MenuController.fct_error(self))
        menuHelp.add_command(
            label="Mise à jour",
            command=lambda: MenuController.maj_fct(self))
        menuHelp.add_separator()
        menuHelp.add_command(
            label="A propos",
            command=lambda: MenuController.show_about(self))

        self.root.config(menu=menuBar)

    def clean_menu_window(self, root):
        for widget in root.winfo_children():
            widget.destroy()
        self.display_menu_window()

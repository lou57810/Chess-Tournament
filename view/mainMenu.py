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
        self.menu_controller = MenuController(self.root)

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

        # =================================== Menu Files ======================================
        menuFile.add_command(label="Gestion Tournoi", command=lambda: self.display_tournament_window())
        menuFile.add_command(label="Enregistrer les résultats", command=lambda: MenuController.param_fct(self))
        menuFile.add_command(label="Impression des rapports", command=lambda: MenuController.fct_warning(self))
        menuFile.add_separator()
        menuFile.add_command(label="Quitter", command=lambda: MenuController.fct_quit(self))

        # ================================== Menu Edition ======================================

        menuEdition.add_command(label="Tous les acteurs alpha", command=lambda:
                                self.menu_controller.display_reports(self.menu_controller.alpha_display_all_players()))
        menuEdition.add_command(label="Tous les acteurs num", command=lambda:
                                self.menu_controller.display_reports(self.menu_controller.num_display_all_players()))

        menuEdition.add_separator()

        # ===============================Getting sub_menus items ================================
        tournament_list = self.menu_controller.display_all_tournaments()

        menu_alpha_tournoi = Menu(menuEdition)
        menuEdition.add_cascade(menu=menu_alpha_tournoi, label="Tous les joueurs d'un tournoi alpha")
        for i in range(len(tournament_list)):
            menu_alpha_tournoi.add_command(label=tournament_list[i],
                                           command=lambda alpha_selected=tournament_list[i]:
                                           self.menu_controller.switch_alpha_item(alpha_selected))

        menu_num_tournoi = Menu(menuEdition)
        menuEdition.add_cascade(menu=menu_num_tournoi, label="Tous les joueurs d'un tournoi num")
        for i in range(len(tournament_list)):
            menu_num_tournoi.add_command(label=tournament_list[i],
                                         command=lambda num_selected=tournament_list[i]:
                                         self.menu_controller.switch_num_item(num_selected))

        # ==========================================================================================
        menuEdition.add_separator()

        menuEdition.add_command(label=" Tous les Tournois", command=lambda: self.menu_controller.display_reports(
            self.menu_controller.display_all_tournaments()))

        # ===========================================================================================
        menu_rounds_tournament = Menu(menuEdition)
        menuEdition.add_cascade(menu=menu_rounds_tournament, label="Toutes les rondes d'un tournoi")
        for i in range(len(tournament_list)):
            menu_rounds_tournament.add_command(label=tournament_list[i],
                                               command=lambda selected=tournament_list[i]:
                                               self.menu_controller.switch_tournament_round(selected))

        menu_matchs_tournament = Menu(menuEdition)
        menuEdition.add_cascade(menu=menu_matchs_tournament, label="Tous les matchs d'un tournoi")
        for i in range(len(tournament_list)):
            menu_matchs_tournament.add_command(label=tournament_list[i],
                                               command=lambda selected=tournament_list[i]:
                                               self.menu_controller.switch_tournament_match(selected))

        menuEdition.add_command(label="Rechercher", command=lambda: MenuController.fct_yes_no(self))

        # =================== Menu Outils =======================
        menuOutils.add_command(label="Parametres", command=lambda: MenuController.param_fct(self))
        menuHelp.add_command(label="Obtenir de l'aide", command=lambda: MenuController.fct_error(self))
        menuHelp.add_command(label="Mise à jour", command=lambda: MenuController.maj_fct(self))
        menuHelp.add_separator()
        menuHelp.add_command(label="A propos", command=lambda: MenuController.show_about(self))

        self.root.config(menu=menuBar)

    def display_tournament_window(self):
        self.clean_menu_window(self.root)
        self.display_menu_window()
        self.tournament_window.display_tournament_window()
        self.tournament_window.tournament_data_set()

    def refresh_tournament_frame(self):
        """Clean root window and display menu"""
        self.display_tournament_window()

    def clean_menu_window(self, root):
        for widget in root.winfo_children():
            widget.destroy()
        self.display_menu_window()

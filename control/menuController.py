import tkinter as tk
from tkinter import Toplevel
from tkinter.ttk import Label
from tkinter import Text
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import showwarning
from tkinter.messagebox import askquestion
from tkinter.messagebox import askyesno
from tinydb import where
from model.dbInterface import Interface


class MenuController:
    def __init__(self, root):
        self.root = root
        self.sort_num_list = list()
        self.alpha_name = list()
        self.num_name = list()
        self.rounds_tournament_list = list()
        self.round_report = list()
        self.match_report = list()
        self.model_interface = Interface()

    def show_about(self):
        about_window = Toplevel(self.root)
        about_window.title("A propos")
        label = Label(about_window, text='Gestion Tournoi d\'echecs \n version 1.0.1')
        label.grid(row=0, column=0, padx=20, pady=20)

    def display_reports(self, data):
        report_window = Toplevel(self.root)
        report_window.geometry("300x400")
        report_window.title("Rapport")
        Toplevel.update(self.root)
        data_text = Text(report_window)
        data_text.delete('1.0', tk.END)
        for string in data:
            data_text.insert(tk.END, string + '\n')
        data_text.pack()

    def maj_fct(self):
        showinfo("showinfo", "Vous êtes à jour !")

    def param_fct(self):
        showinfo("showinfo", "Passez à la version 1.1.2")

    def fct_error(self):
        showerror("showerror", "En maintenance")

    def fct_warning(self):
        showwarning("showarning", "Avertissement, imprimante non trouvée")

    def fct_yes_no(self):  # résultat en console
        question = askquestion("Etes vous satisfait ?:")
        if question == "yes":
            showinfo("showinfo", "Ok Merci !")
        else:
            showinfo("showinfo", "Nouvelle recherche !")

    def fct_quit(self):
        if askyesno('Quitter ?'):
            self.root.quit()
    # =============== display tournaments interface  ==============

    def display_tournament_window(self):
        self.clean_menu_window(self.root)
        self.display_menu_window()
        self.tournament_window.display_tournament_window()
        self.tournament_window.tournament_data_set()

    # ================== reports ====================
    # 1.
    def alpha_display_all_players(self):
        serialized_players = self.model_interface.set_db_players_all()
        alpha_list = list()
        for elt in serialized_players:
            alpha_list.append(elt['first_name'] + ' ' + elt['last_name'])
        print("\n")
        return sorted(alpha_list)

    # 2.
    def num_display_all_players(self):
        serialized_players = self.model_interface.set_db_players_all()
        num_list = list()
        for elt in serialized_players:
            num_list.append([elt['first_name'] + ' ' + elt['last_name'], elt['rank']])
        num_list.sort(key=lambda x: x[1])
        self.sort_num_list = list()

        for elt in num_list:
            elt = (elt[0] + ' ' + elt[1])
            self.sort_num_list.append(elt)
        print("\n")
        return self.sort_num_list

    def switch_alpha_item(self, alpha_selected):
        self.alpha_display_one_tournament_players(alpha_selected)

    def switch_num_item(self, num_selected):
        self.num_display_one_tournament_players(num_selected)

    def switch_tournament_round(self, selected):
        self.display_rounds_tournament(selected)

    def switch_tournament_match(self, selected):
        self.display_matchs_tournament(selected)

    def alpha_display_one_tournament_players(self, alpha_selected):
        players_table = self.model_interface.set_db_players_env()
        tournament_name = alpha_selected
        serialized_tournament_players = players_table.search(where('tournament_name') == tournament_name)
        i = 0
        for i in range(len(serialized_tournament_players)):
            self.alpha_name.append(
                serialized_tournament_players[i]['first_name'] + ' ' + serialized_tournament_players[i]['last_name'])
            i += 1

        self.display_reports(sorted(self.alpha_name))
        self.alpha_name.clear()

    def num_display_one_tournament_players(self, num_selected):
        players_table = self.model_interface.set_db_players_env()
        tournament_name = num_selected
        serialized_tournament_players = players_table.search(where('tournament_name') == tournament_name)
        i = 0
        for i in range(len(serialized_tournament_players)):
            self.num_name.append([serialized_tournament_players[i]['first_name'] + ' ' +
                                  serialized_tournament_players[i]['last_name'],
                                  serialized_tournament_players[i]['rank']])
            i += 1

        self.num_name.sort(key=lambda x: x[1])
        self.sort_num_list = list()

        for elt in self.num_name:
            elt = (elt[0] + ' ' + elt[1])
            self.sort_num_list.append(elt)
        self.display_reports(self.sort_num_list)
        self.num_name.clear()
        self.sort_num_list.clear()

    def display_all_tournaments(self):
        serialized_tournaments = self.model_interface.set_db_tournaments_all()
        tournament_list = list()
        for elt in serialized_tournaments:
            tournament_list.append(elt['tournament_name'])
        return tournament_list

    def display_rounds_tournament(self, selected):
        tournaments_table = self.model_interface.set_db_tournaments_env()
        tournament_name = selected
        Toplevel.update(self.root)
        serialized_tournaments = tournaments_table.search(where('tournament_name') == tournament_name)
        round_list = serialized_tournaments[0]['rounds_lists']
        self.display_round_report(round_list)
        self.round_report.clear()

    def display_matchs_tournament(self, selected):
        tournaments_table = self.model_interface.set_db_tournaments_env()
        tournament_name = selected
        Toplevel.update(self.root)
        serialized_tournaments = tournaments_table.search(where('tournament_name') == tournament_name)  # list ??
        round_list = serialized_tournaments[0]['rounds_lists']
        self.display_matchs_report(round_list)
        self.match_report.clear()

    def display_round_report(self, data):
        report_window = Toplevel(self.root)
        report_window.geometry("600x400")
        report_window.title("Rapport rondes par tournois")
        i = 0
        while i < len(data):
            j = 2
            self.round_report.append(data[i][0])
            self.round_report.append(" : ")
            self.round_report.append(data[i][1])
            self.round_report.append(" : ")
            self.round_report.append("\n")

            while j < 6:
                self.round_report.append(data[i][j][0][0])
                self.round_report.append(" ")
                self.round_report.append(data[i][j][0][1])
                self.round_report.append(" :: ")
                self.round_report.append(data[i][j][1][0])
                self.round_report.append(" ")
                self.round_report.append(data[i][j][1][1])
                self.round_report.append("\n")
                j += 1

            self.round_report.append(data[i][6])
            self.round_report.append("\n")
            i += 1

        data_text = Text(report_window)
        for string in self.round_report:
            data_text.insert(tk.END, string)
        data_text.pack()

    def display_matchs_report(self, data):
        report_window = Toplevel(self.root)
        report_window.geometry("600x400")
        report_window.title("Rapport Matchs par tournois")

        self.match_report = list()
        for elt in data:
            i = 2
            while i < 6:
                self.match_report.insert(0, elt[i][0][0])
                self.match_report.insert(1, " ")
                self.match_report.insert(2, elt[i][0][1])
                self.match_report.insert(3, " :: ")
                self.match_report.insert(4, elt[i][1][0])
                self.match_report.insert(5, " ")
                self.match_report.insert(6, elt[i][1][1])
                self.match_report.insert(7, "\n")
                i += 1

        data_text = Text(report_window)
        for elt in self.match_report:
            data_text.insert(tk.END, elt)
        data_text.pack()

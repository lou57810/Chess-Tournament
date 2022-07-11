from tkinter import Toplevel
from tkinter.ttk import Label
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import showwarning
from tkinter.messagebox import askquestion
from tkinter.messagebox import askyesno


class MenuController:
    def __init__(self, root):
        self.root = root

    def show_about(self):
        about_window = Toplevel(self.root)
        about_window.title("A propos")
        lb = Label(about_window,
                   text='Gestion Tournoi d\'echecs \n version 1.0.1')
        lb.grid(row=0, column=0, padx=20, pady=20)

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

    def display_tournament_window(self):
        self.clean_menu_window(self.root)
        self.display_menu_window()
        self.tournament_window.display_tournament_window()
        self.tournament_window.tournament_data_set()

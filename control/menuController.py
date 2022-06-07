from tkinter import *
from tkinter.messagebox import *

#from view.playerView import PlayerView


class MenuController:
    def __init__(self,root):
        self.root = root

    def show_about(self):
        about_window = Toplevel(self.root)
        about_window.title("A propos")
        lb = Label(about_window, text='Gestion Tournoi d\'echecs \n version 1.0.1')
        lb.grid(row=0, column=0, padx=20, pady=20)

    def maj_fct(self):
        showinfo("showinfo", "Vous êtes à jour !")

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
        self.tournament_window.display_tournament_window()     #tournament_data_frame
        self.tournament_window.tournament_data_set()      #tournament_management_frame()

    """

    def display_player_window(self):
        self.clean_menu_window(self.root)
        from view.mainMenu import MainMenu
        main_menu = MainMenu(self.root)
        main_menu.display_menu_window()
        #self.display_menu_window()
        self.player_window.display_player_window()
        self.player_window.player_data_set(t)

    def clean_menu_window(self, root):
        from view.mainMenu import MainMenu
        main_menu = MainMenu(self.root)
        for widget in root.winfo_children():
            widget.destroy()
        main_menu.display_menu_window()

    
    def bind_player_window(self):
        self.clean_menu_window(self.root)
        self.display_menu_window()
        self.player_window.display_player_window()
        self.player_window.player_data_get()
    


    def clean_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        #self.display_menu_window()
    """




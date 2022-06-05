from tkinter import *
from view.mainMenu import MainMenu


class Window:
    def __init__(self):
        pass

    def init_window(self):
        root = Tk()
        root.title('Gestion Tournoi d\'echecs')
        root.geometry("1024x860")
        root.config(background='#9a031e')
        root.iconbitmap("./img/logo.ico")
        root.option_add('*tearOff', FALSE)  # Supprime le séparateur

        # menu view creation
        menu = MainMenu(root)
        menu.display_menu_window()
        root.mainloop()
        return root



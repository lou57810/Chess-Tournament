from tkinter import Tk
# from tkinter import *
# import tkinter as tk
import os
from view.mainMenu import MainMenu


class Window:
    def __init__(self):
        pass

    def init_window(self):
        root = Tk()
        root.title('Gestion Tournoi d\'echecs')
        root.geometry("1280x860")
        root.config(background='#9a031e')

        if "nt" == os.name:
            root.iconbitmap("./img/logo.ico")
        else:
            root.wm_iconbitmap(bitmap="@./img/logo.xbm")
        root.option_add('*tearOff', False)  # Supprime le séparateur

        # menu view creation
        menu = MainMenu(root)
        menu.display_menu_window()
        root.mainloop()
        return root

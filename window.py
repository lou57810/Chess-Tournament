<<<<<<< HEAD
from tkinter import Tk
=======
from tkinter import *
import tkinter as tk
import os
>>>>>>> 965571086e465a4eec4d9032c9e52355da4c5010
from view.mainMenu import MainMenu


class Window:
    def __init__(self):
        pass

    def init_window(self):
        root = Tk()
        #root = Tk()
        root.title('Gestion Tournoi d\'echecs')
        root.geometry("1280x860")
        root.config(background='#9a031e')
<<<<<<< HEAD
        root.iconbitmap("./img/logo.ico")
        root.option_add('*tearOff', False)  # Supprime le séparateur
=======
        if "nt" == os.name:
            root.iconbitmap("./img/logo.ico")
        else:        
            root.wm_iconbitmap(bitmap = "@./img/logo.xbm")        
        
        root.option_add('*tearOff', FALSE)  # Supprime le séparateur
        print("os:", os.name)
>>>>>>> 965571086e465a4eec4d9032c9e52355da4c5010

        # menu view creation
        menu = MainMenu(root)
        menu.display_menu_window()
        root.mainloop()
        return root
<<<<<<< HEAD
=======




>>>>>>> 965571086e465a4eec4d9032c9e52355da4c5010

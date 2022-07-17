import tkinter as tk

from view.mainMenu import MainMenu


class Window:
    def __init__(self):
        pass

    def init_window(self):
        root = tk.Tk()
        root.title('Gestion Tournoi d\'echecs')
        root.geometry("1280x860")
        root.config(background='#9a031e')
        root.iconbitmap("./img/logo.ico")
        root.option_add('*tearOff', tk.FALSE)  # Supprime le séparateur

        # menu view creation
        menu = MainMenu(root)
        menu.display_menu_window()
        root.mainloop()
        return root

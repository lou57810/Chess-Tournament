import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import *
from view.playerView import PlayerView
from view.tournamentView import TournamentView
from view.roundView import RoundView

class MainMenu:

	def __init__(self,root_window):
		self.root_window = root_window

		self.playerFrame = Frame(self.root_window, width=1024, height=760, bg='#fff2cc')
		self.tourFrame = Frame(self.root_window, width=1024, height=760, bg='#400000')
		self.roundFrame = Frame(self.root_window, width=1024, height=960, bg='#9a031e')




	def draw_mainMenuView(self):
		root_window = Tk()
		root_window.title('Gestion Tournoi d\'echecs')
		root_window.geometry("1024x860")
		root_window.config(background='#9a031e')
		root_window.iconbitmap("./img/logo.ico")
		root_window.option_add('*tearOff', FALSE)	# Supprime le séparateur



		#self.displayMenu(self.root_window)
		menu = MainMenu(root_window)
		menu.displayMenu()
		root_window.mainloop()
		return root_window

	def displayMenu(self):
		#root_window = WinMenu.root_window
		menuBar = Menu(self.root_window)

		menuFile = Menu(menuBar)
		menuEdition = Menu(menuBar)
		menuOutils = Menu(menuBar)
		menuHelp = Menu(menuBar)

		menuBar.add_cascade(label = "Fichier", menu=menuFile)
		menuBar.add_cascade(label = "Edition", menu=menuEdition)
		menuBar.add_cascade(label = "Outils", menu=menuOutils)
		menuBar.add_cascade(label = "?", menu=menuHelp)

		# Commands
		menuFile.add_command(label="Gestion Tournoi",command=lambda: self.display_tourWindow(self.tourFrame))
		menuFile.add_command(label="Afficher les resultats")
		menuFile.add_command(label="Enregistrer les résultats")
		menuFile.add_command(label="Modifier les resultats")
		menuFile.add_separator()
		menuFile.add_command(label="Quitter", command=quit)

		menuEdition.add_command(label="Edition du rapport")
		menuEdition.add_command(label="Impression du rapport")#,command=self.fctWarning)
		menuEdition.add_separator()
		menuEdition.add_command(label="Rechercher")#,command=self.fctYesNo)

		menuOutils.add_command(label="Gestion Joueurs",command=lambda: self.display_playerWindow(self.playerFrame))
		menuOutils.add_command(label="Gestion rondes",command=lambda: self.display_roundWindow(self.roundFrame))
		

		menuHelp.add_command(label="Obtenir de l'aide")#, command=self.fctError)
		menuHelp.add_command(label="Mise à jour")#,command=self.majFct)
		menuHelp.add_separator()
		menuHelp.add_command(label="A propos")#,command=self.show_about)

		self.root_window.config(menu=menuBar)


		

	def display_playerWindow(self,root_window):
		self.clean_window(self.root_window)
		PlayerView.playerView(self,self.playerFrame)

	def display_tourWindow(self,root_window):
		self.clean_window(self.root_window)
		TournamentView.tourView(self,self.tourFrame)

	def display_roundWindow(self,root_window):
		self.clean_window(self.root_window)
		RoundView.roundView(self,self.roundFrame)

	
	def clean_window(self,root_window):
		for widget in root_window.winfo_children():
			widget.destroy()			
		self.displayMenu()

	


		
		
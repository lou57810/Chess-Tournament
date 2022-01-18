import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from view.playView import PlayerWindow
from view.tourView import TourWindow
from view.roundView import RoundWindow
#from model.round import Round
#from controller.control import Control
#from PIL import ImageTk,Image
#from view.turnViewManager import TournamentManager
#from view.playerViewManager import PlayerManager



class WinMenu:
	def __init__(self):
		
		self.root = Tk()				
		self.root.title('Gestion Tournoi')
		self.root.geometry("1024x760")		
		self.root.config(background='grey')
		self.root.iconbitmap("./img/logo.ico")
		self.root.option_add('*tearOff', FALSE)	# Supprime le séparateur
		
		self.displayMenu()
		
		self.playerFrame = Frame(self.root,width=1024,height=760,bg='#fff2cc')		
		self.tourFrame   = Frame(self.root,width=1024,height=760,bg='#400000')
		self.roundFrame  = Frame(self.root,width=1024,height=760,bg='#b2dc76')
		
		self.root.mainloop()		

	def displayMenu(self):		
		menuBar = Menu(self.root)		

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
		menuFile.add_command(label="Gestion Joueurs",command=lambda: self.display_playerWindow(self.playerFrame))
		menuFile.add_command(label="Gestion rondes",command=lambda: self.display_roundWindow(self.roundFrame))
		menuFile.add_command(label="Afficher les resultats")
		menuFile.add_command(label="Enregistrer les résultats")
		menuFile.add_command(label="Modifier les resultats")
		menuFile.add_separator()
		menuFile.add_command(label="Quitter", command=quit)

		menuEdition.add_command(label="Edition du rapport")
		menuEdition.add_command(label="Impression du rapport")#,command=self.fctWarning)
		menuEdition.add_separator()
		menuEdition.add_command(label="Rechercher")#,command=self.fctYesNo)

		menuOutils.add_command(label="Génération des paires")
		menuOutils.add_command(label="Créer un tour(Round(n))")

		menuHelp.add_command(label="Obtenir de l'aide")#, command=self.fctError)
		menuHelp.add_command(label="Mise à jour")#,command=self.majFct)
		menuHelp.add_separator()
		menuHelp.add_command(label="A propos")#,command=self.show_about)

		self.root.config(menu=menuBar)
		

	def display_playerWindow(self,root):		
		self.clean_window(self.root)
		PlayerWindow.playerView(self,self.playerFrame)

	def display_tourWindow(self,root):		
		self.clean_window(self.root)						
		TourWindow.tourView(self,self.tourFrame)

	def display_roundWindow(self,root):		
		self.clean_window(self.root)						
		RoundWindow.roundView(self,self.roundFrame)
		
	
	def clean_window(self,root):		
		for widget in root.winfo_children():			
			widget.destroy()			
		self.displayMenu()

	


		
		
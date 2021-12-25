import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
#from controller.control import Control
#from PIL import ImageTk,Image
from view.turnViewManager import TournamentManager
from view.playerViewManager import PlayerManager


class WinMenu():		

	def __init__(self,wt=TournamentManager):
		
		self.root = Tk()		
		self.root.title('Gestion Tournoi')
		self.root.geometry("900x760")		
		#self.root.config(background='brown')
		self.root.iconbitmap("./img/logo.ico")
		self.root.option_add('*tearOff', FALSE)	# Supprime le séparateur
		#self.turnManagement = TournamentManager(self.root)
		#self.turnManagement = TournamentManager(self)
		self.wt = self.root
		#self.w = TournamentManager
		self.displayMenu()

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
		menuFile.add_command(label="Gestion Tournoi",command=lambda: self.display_tournament_manager())
		menuFile.add_command(label="Gestion joueurs",command=lambda: self.display_player_manager())
		menuFile.add_command(label="Afficher les resultats")
		menuFile.add_command(label="Enregistrer les résultats")
		menuFile.add_command(label="Modifier les resultats")
		menuFile.add_separator()
		menuFile.add_command(label="Quitter", command=quit)

		menuEdition.add_command(label="Edition du rapport")
		menuEdition.add_command(label="Impression du rapport",command=self.fctWarning)
		menuEdition.add_separator()
		menuEdition.add_command(label="Rechercher",command=self.fctYesNo)

		menuOutils.add_command(label="Génération des paires")
		menuOutils.add_command(label="Créer un tour(Round(n))")

		menuHelp.add_command(label="Obtenir de l'aide", command=self.fctError)
		menuHelp.add_command(label="Mise à jour",command=self.majFct)
		menuHelp.add_separator()
		menuHelp.add_command(label="A propos",command=self.show_about)

		#turnManagement()
		
		
		self.root.config(menu=menuBar)
		self.root.mainloop()

	#========================== Fcts ==============================

	def show_about(self):
		about_window = Toplevel(self.root)
		about_window.title("A propos")
		lb = Label(about_window,text='Gestion Tournoi d\'echecs \n version 1.0.1')
		lb.grid(row=0,column=0, padx=20,pady=20)		

	def majFct(self):
		showinfo("showinfo","Vous êtes à jour !")

	def fctError(self):
		showerror("showerror","En maintenance")

	def fctWarning(self):
		showwarning("showarning","Avertissement, imprimante non trouvée")
	
	def fctYesNo(self):			# résultat en console
		question = askquestion("Etes vous satisfait ?:")
		if question == "yes":		
			print("Ok, merci")
		else:
			print("Recommencez !")

	def display_tournament_manager(self):		
		#self.clean_window(self.root)
		TournamentManager.tournamentFrameManager(self)

	def display_player_manager(self):
		#self.clean_window(self.root)
		PlayerManager.playerFrameManager(self)
	"""
	def clean_window(self,root):		
		for widget in root.winfo_children():
			widget.destroy()
		self.displayMenu()        	
	
	def playerManagement(self):
		playerFrame = Frame(self.root,width=1024,height=760,bg="red")
		playerFrame.pack(fill="both",expand=1)
	
	def turnManagement(self):
		tournamentWindow = TournamentManager()
		playerFrame = Frame(self.root,width=1024,height=760,bg="blue")
		playerFrame.pack(fill="both",expand=1)
	"""


	
	
	

				

		
	
import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
from tinydb import TinyDB, Query, where
from tkinter import messagebox
from control.controller import Controller
from model.player import Player
from model.round import Round



class RoundWindow:
	def __init__(self):		
		self.date = None
	
	def roundView(self,roundFrame):
		# Create a Treeview Frame						
		roundFrame.pack(padx=5,pady=20)
		tree_frame = ttk.Treeview(roundFrame)

	# ==========================Database============================		

		db = TinyDB('data/db_tournaments.json')	
		players_table = db.table('round')

	# ===========================Style & frames=============================
		style = ttk.Style()
		# Pick a theme
		#print(style.theme_names())  : themes disponibles pour Tk
		style.theme_use("alt")
		style.configure("Treeview",
			background="white",
			foreground="black",
			rowheight=25,
			fieldbackground="white"
		)
		# Change selected color
		style.map("Treeview",background=[("selected","brown")])

		# Create a Treeview Scrollbar
		tree_scroll = Scrollbar(roundFrame)
		tree_scroll.pack(side=RIGHT,fill=Y)

		# Configure the Scrollbar
		tree_frame = ttk.Treeview(roundFrame,yscrollcommand=tree_scroll.set,select="extended")
		
		tree_scroll.config(command=tree_frame.yview)

		# Define Columns
		tree_frame["columns"] = ("matchs","player_white","score_white","player_black","score_black","startTime","endTime")

		# Create Striped Row Tags
		tree_frame.tag_configure('oddrow',background="#ecdab9")
		tree_frame.tag_configure('evenrow',background="#a47053")
		tree_frame.pack(padx=50,pady=20)

# ===================== Fcts =================================

		def genRound():
			pass

		def startMatch():
			date = Controller.getTime()
			startPrint_label = Label(data_frame,text=date)
			startPrint_label.grid(row=2,column=1,padx=40,pady=10)

		def endMatch():
			date = Controller.getTime()
			endPrint_label = Label(data_frame,text=date)
			endPrint_label.grid(row=2,column=2,padx=40,pady=10)

		def remove_all_Records():
			response = messagebox.askyesno("Cette opération est irréversible!!")	
			round_table = db.table('round')
			if response == 1:
				# Clear the treeview
				for record in tree_frame.get_children():
					tree_frame.delete(record)
					#print("records",record)
				players_table.truncate()
		"""
		def query_database():	
			global count
			count = 0	
			round_table = db.table('rounds')	
			records = round_table.all()

			n = 0	
			for record in records:
				if n % 2 == 0:		
					tree_frame.insert(parent="",index=n,iid=n,text='',
						values=(
						records[n]['matchs']								
						records[n]['player_white'],
						records[n]['score_white'],
						records[n]['player_black'],
						records[n]['score_black'],
						records[n]['startTime'],
						records[n]['endTime']
						records[n]['rank']),
					tags=('evenrow',))
					
				else:
					tree_frame.insert(parent="",index=n,iid=n,text='',
						values=(				
						records[n]['matchs']								
						records[n]['player_white'],
						records[n]['score_white'],
						records[n]['player_black'],
						records[n]['score_black'],
						records[n]['startTime'],
						records[n]['endTime']
						records[n]['rank']),				
					tags=('oddrow',))
				n += 1
		"""
		

		

# =====================Fill the Treeview======================		
		
		# Format columns
		tree_frame.column("#0",width=0,stretch=NO)
		tree_frame.column("matchs",anchor=W,width=50)
		tree_frame.column("player_white",anchor=CENTER,width=130)
		tree_frame.column("score_white",anchor=CENTER,width=130)
		tree_frame.column("player_black",anchor=CENTER,width=130)
		tree_frame.column("score_black",anchor=CENTER,width=120)
		tree_frame.column("startTime",anchor=CENTER,width=100)
		tree_frame.column("endTime",anchor=CENTER,width=100)
		

		# Create headings
		tree_frame.heading("#0",text="",anchor=W)	
		tree_frame.heading("matchs",text="Matchs",anchor=CENTER)
		tree_frame.heading("player_white",text="Joueur blanc",anchor=CENTER)
		tree_frame.heading("score_white",text="Score",anchor=CENTER)
		tree_frame.heading("player_black",text="Joueur noir",anchor=CENTER)
		tree_frame.heading("score_black",text="Score",anchor=CENTER)
		tree_frame.heading("startTime",text="Horaire début",anchor=CENTER)
		tree_frame.heading("endTime",text="Horaire fin",anchor=CENTER)
		

# ================Add Management Entries Boxes=================
		data_frame = LabelFrame(roundFrame,text="Gestion des rondes")
		data_frame.pack(fill="x",padx=30,pady=20)

		# Labels		
		gen_button = Button(data_frame,text="Générer une ronde",command=Round.getPlayerDatas())
		gen_button.grid(row=1,column=0,padx=10,pady=20)

		startButton = Button(data_frame,text="Début du match",command=startMatch)
		startButton.grid(row=1,column=1,padx=10,pady=10)
		

		
		endButton = Button(data_frame,text="Fin du match",command=endMatch)
		endButton.grid(row=1,column=2,padx=10,pady=10)
		

		regWhiteButton = Button(data_frame,text="Total joueur blanc")
		regWhiteButton.grid(row=1,column=5,padx=10,pady=10)

		regBlackButton = Button(data_frame,text="Total joueur noir")
		regBlackButton.grid(row=1,column=6,padx=10,pady=10)

		spinWhite_label = Label(data_frame,text="Score joueur blanc")
		spinWhite_label.grid(row=2,column=0,padx=0,pady=10)
		
		class_WspinBox = Spinbox(data_frame,values=(0,0.5,1),font=("helvetica",10),width=4)
		class_WspinBox.grid(row=3,column=0,padx=10,pady=10)

		spinBlack_label = Label(data_frame,text="Score joueur noir")
		spinBlack_label.grid(row=2,column=1,padx=5,pady=10)

		class_BspinBox = Spinbox(data_frame,values=(0,0.5,1),font=("helvetica",10),width=4)
		class_BspinBox.grid(row=3,column=1,padx=10,pady=10)

		scoreWhiteBox = Entry(data_frame,width=25)
		scoreWhiteBox.grid(row=2,column=5,padx=10,pady=10)

		scoreBlackBox = Entry(data_frame,width=25)
		scoreBlackBox.grid(row=2,column=6,padx=10,pady=10)

		rm_all_button = Button(data_frame,text="Supprimer tout",command=remove_all_Records)
		rm_all_button.grid(row=3,column=7,padx=10,pady=20)				

		quit_button = Button(data_frame,text="Quitter",command=lambda: self.quitRoundView())				
		quit_button.grid(row=3,column=8,padx=20,pady=20)

		#query_database()




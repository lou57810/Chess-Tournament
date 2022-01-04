import tkinter as tk
from tkinter import *
from tkinter import ttk
import time



class RoundWindow:
	def __init__(self):		
		self.date = None
	
	def roundView(self,roundFrame):
		# Create a Treeview Frame						
		roundFrame.pack(padx=5,pady=20)
		tree_frame = ttk.Treeview(roundFrame)

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

		def getStartDate():			
			date = time.strftime('%d/%m/%y %H:%M:%S',time.localtime())
			startPrint_label = Label(data_frame,text=date)
			startPrint_label.grid(row=2,column=1,padx=40,pady=10)

		def getEndDate():			
			date = time.strftime('%d/%m/%y %H:%M:%S',time.localtime())
			endPrint_label = Label(data_frame,text=date)
			endPrint_label.grid(row=2,column=2,padx=40,pady=10)

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
		gen_button = Button(data_frame,text="Générer une ronde")
		gen_button.grid(row=1,column=0,padx=10,pady=20)

		startButton = Button(data_frame,text="Début du match",command=getStartDate)
		startButton.grid(row=1,column=1,padx=10,pady=10)
		
		endButton = Button(data_frame,text="Fin du match",command=getEndDate)
		endButton.grid(row=1,column=2,padx=10,pady=10)

		regButton = Button(data_frame,text="Enregistrer")
		regButton.grid(row=1,column=4,padx=10,pady=10)
		
		#startBox = Entry(data_frame,width=25,text=date)		
		#startBox.grid(row=2,column=1,padx=10,pady=10)
		
		#endTime_label = Label(data_frame,text="Date heure fin")
		#endTime_label.grid(row=0,column=2,padx=10,pady=10)
		
		finalScore_label = Label(data_frame,text="Saisie manuelle des résultats")
		finalScore_label.grid(row=0,column=4,padx=5,pady=10)
		finalBox = Entry(data_frame,width=25)
		finalBox.grid(row=2,column=4,padx=10,pady=10)
		

		# Logical Entry boxes
		#genBox = Entry(data_frame,width=25)
		#genBox.grid(row=1,column=1,padx=10,pady=10)
		
		
				
		


		quit_button = Button(data_frame,text="Quitter",command=lambda: self.quitRoundView())				
		quit_button.grid(row=1,column=5,padx=20,pady=20)

# ================Button Commands(rm = remove)======================
		

		

		

		
"""
		#add_button = Button(button_frame,text="Ajouter",command=add_Entries)
		#add_button.grid(row=0,column=0,padx=10,pady=20)

		modif_button = Button(button_frame,text="Modifier",command=update_one_record) 
		modif_button.grid(row=0,column=1,padx=10,pady=20)

		rm_one_button = Button(button_frame,text="Supprimer",command=remove_One_Entry)
		rm_one_button.grid(row=0,column=2,padx=10,pady=20)

		rm_all_button = Button(button_frame,text="Supprimer tout",command=remove_all_Records)
		rm_all_button.grid(row=0,column=3,padx=10,pady=20)

		clear_button = Button(button_frame,text="Clear",command=clear_Entries)
		clear_button.grid(row=0,column=5,padx=10,pady=20)

		quit_button = Button(button_frame,text="Quitter",command=lambda: self.quitTourView())				
		quit_button.grid(row=0,column=7,padx=10,pady=20)

		# Bind the treeview
		tree_frame.bind("<ButtonRelease-1>",selectEntry)

		radio_frame.pack()
"""

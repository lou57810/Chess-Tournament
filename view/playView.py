import tkinter as tk
from tkinter import *
from tkinter import ttk
import PIL
from PIL import ImageTk,Image
from tkinter import messagebox
from tkcalendar import *
#import sqlite3
from tinydb import TinyDB, Query,where
from tinydb.operations import delete
from model.player import Player
from model.round import Round
import pprint




class PlayerWindow:
	def __init__(self,root):		
		#self.playerFields = ("id","first_name","last_name","birth_date","gender","rank")
		pass
		
	def playerView(self,playerFrame):
		playerFields = ("Id","first_name","last_name","birth_date","gender","rank")
		playerFrame = Frame(self.root)
		playerFrame.pack(pady=20)
		tree_frame = ttk.Treeview(playerFrame)

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
		style.map("Treeview",background=[("selected","blue")])

		# Create a Treeview Scrollbar
		tree_scroll = Scrollbar(playerFrame)
		tree_scroll.pack(side=RIGHT,fill=Y)

		# Configure the Scrollbar
		tree_frame = ttk.Treeview(playerFrame,yscrollcommand=tree_scroll.set,select="extended")
		tree_frame.pack(pady=20)
		tree_scroll.config(command=tree_frame.yview)

		# Define Columns
		tree_frame["columns"] = playerFields

		# Create Striped Row Tags
		#tree_frame.tag_configure('oddrow',background="#ecdab9")
		#tree_frame.tag_configure('evenrow',background="#a47053")

		count = 0

		# ==========================Database============================		

		db = TinyDB('data/db_tournaments.json')	
		players_table = db.table('players')
		serialized_players = players_table.all()

		rounds_table = db.table('rounds')
		serialized_rounds = rounds_table.all()

		# ===========================Fcts ==============================
		def add_Entries():

			global count
			
			tree_frame.tag_configure('oddrow',background="#ecdab9")
			tree_frame.tag_configure('evenrow',background="#a47053")
			# Output to entry boxes
			count = len(tree_frame.get_children())
			
			if count % 2 == 0:
				tree_frame.insert(parent="",index='end',iid=count,text="",values=(
					idSpinBox.get(),											
					f_nameBox.get(),
					l_nameBox.get(),			
					date_Box.get_date(),
					gender.get(),				
					class_spinBox.get()),
					tags=('evenrow',)
					)

			else:
				tree_frame.insert(parent="",index='end',iid=count,text="",values=(
					idSpinBox.get(),								
					f_nameBox.get(),
					l_nameBox.get(),			
					date_Box.get_date(),
					gender.get(),				
					class_spinBox.get()),
					tags=('oddrow',)
						)
			count +=1
			#getDbIndex()
			register_dataPlayers()	# Filling identity playersDB
			register_rankPlayers()
			clear_Entries()			
			
		def register_dataPlayers():	
			players_table = db.table('players')				
			print("index: ",players_table.insert({
					'id': idSpinBox.get(),														
					'first_name': f_nameBox.get(),
					'last_name': l_nameBox.get(),			
					'birth_date': date_Box.get(),
					'gender': gender.get(),
					'rank': class_spinBox.get()
					}))

		
			
		def register_rankPlayers():
			rounds_table = db.table('rounds')
			rounds_table.insert({
					'id': idSpinBox.get(),
					'first_name': f_nameBox.get(),
					'last_name': l_nameBox.get(),												
					'rank': class_spinBox.get()
				})
		

		def query_database():	
			global count
			count = 0
			tree_frame.tag_configure('oddrow',background="#ecdab9")
			tree_frame.tag_configure('evenrow',background="#a47053")	
			players_table = db.table('players')	
			serialized_players = players_table.all()

			n = 0	
			for record in serialized_players:
				if n % 2 == 0:		
					tree_frame.insert(parent="",index=n,iid=n,text='',
						values=(
						serialized_players[n]['id'],							
						serialized_players[n]['first_name'],
						serialized_players[n]['last_name'],
						serialized_players[n]['birth_date'],
						serialized_players[n]['gender'],
						serialized_players[n]['rank']),
					tags=('evenrow',))
					
				else:
					tree_frame.insert(parent="",index=n,iid=n,text='',
						values=(
						serialized_players[n]['id'],				
						serialized_players[n]['first_name'],
						serialized_players[n]['last_name'],
						serialized_players[n]['birth_date'],
						serialized_players[n]['gender'],
						serialized_players[n]['rank']),				
					tags=('oddrow',))
				
				n += 1

			
		# Update records: delete all & rewrite ?
		def update_one_record():
						
			selected = tree_frame.focus()			
			value = tree_frame.item(selected,'values')			
			tree_frame.delete(selected)

			players_table = db.table('players')			
			rounds_table = db.table('rounds')
			serialized_players = players_table.all()
			serialized_rounds = rounds_table.all()

			User = Query()			
			print(rounds_table.search(User.id == value[0]))
			
			players_table.update({'id': idSpinBox.get()},User.id==value[0])
			players_table.update({'first_name': f_nameBox.get()},User.id==value[0])
			players_table.update({'last_name': l_nameBox.get()},User.id==value[0])
			players_table.update({'birth_date': date_Box.get()},User.id==value[0])
			players_table.update({'gender': gender.get()},User.id==value[0])
			players_table.update({'rank': class_spinBox.get()},User.id==value[0])

			rounds_table.update({'id': idSpinBox.get()},User.id==value[0])
			rounds_table.update({'first_name': f_nameBox.get()},User.id==value[0])
			rounds_table.update({'last_name': l_nameBox.get()},User.id==value[0])												
			rounds_table.update({'rank': class_spinBox.get()},User.id==value[0])

			tree_frame.insert(parent="",index='end',iid=value[0],text="",values=(
					idSpinBox.get(),											
					f_nameBox.get(),
					l_nameBox.get(),			
					date_Box.get_date(),
					gender.get(),				
					class_spinBox.get()))
			

		def remove_one_record():
			clear_Entries()
			x = tree_frame.selection()[0]
			selected = tree_frame.focus()			
			value = tree_frame.item(selected,'values')
			tree_frame.delete(x)				
			
			players_table = db.table('players')			
			rounds_table = db.table('rounds')
			
			User = Query()
			players_table.remove(User.id == value[0])
			rounds_table.remove(User.id == value[0])

			messagebox.showinfo("Deleted!", "Your record is deleted")

		def remove_all_Records():
			response = messagebox.askyesno("Cette opération est irréversible!!")	
			players_table = db.table('players')
			rounds_table = db.table('rounds')
			if response == 1:
				# Clear the treeview
				for records in tree_frame.get_children():
					tree_frame.delete(records)					
				players_table.truncate()
				rounds_table.truncate()

		def clear_Entries():
			idSpinBox.delete(0,END)			
			f_nameBox.delete(0,END)
			l_nameBox.delete(0,END)	
			date_Box.delete(0,END)	
			gender.set(None)	# gender.deselect() don't work		
			class_spinBox.delete(0,END)
			
		# Select one Entry
		def selectEntry(e):
			clear_Entries()
			# Grab record Number
			selected = tree_frame.focus()
			
			# Grab record values
			values = tree_frame.item(selected,'values')
			idSpinBox.insert(0,values[0])		
			f_nameBox.insert(0,values[1])
			l_nameBox.insert(0,values[2])	
			date_Box.insert(0,values[3])

			# ==========RadioBtn===========
			if values[4] == "Homme":		
				gender_BoxH.invoke()
				
			elif values[4] == "Femme":		
				gender_BoxF.invoke()
			# =============================
			
			class_spinBox.insert(0,values[5])

		def quitPlayerWindow():			
			playerFrame.destroy()

		# =====================Fill the Treeview======================		
		
		# Format columns
		tree_frame.column("#0",width=0,stretch=NO)
		tree_frame.column("Id",anchor=W,width=10)
		tree_frame.column("first_name",anchor=W,width=130)
		tree_frame.column("last_name",anchor=W,width=130)
		tree_frame.column("birth_date",anchor=CENTER,width=130)
		tree_frame.column("gender",anchor=CENTER,width=120)
		tree_frame.column("rank",anchor=CENTER,width=130)

		# Create headings
		tree_frame.heading("#0",text="",anchor=W)
		tree_frame.heading("Id",text="Id",anchor=W)	
		tree_frame.heading("first_name",text="Nom",anchor=W)
		tree_frame.heading("last_name",text="Prénom",anchor=W)
		tree_frame.heading("birth_date",text="Date de naissance",anchor=CENTER)
		tree_frame.heading("gender",text="Sexe H/F",anchor=CENTER)
		tree_frame.heading("rank",text="Elo",anchor=CENTER)

		# ================Add Management Entries Boxes=================
		data_frame = LabelFrame(playerFrame,text="Management Joueurs")
		data_frame.pack(fill="x",padx=20,pady=20)

		# Labels
		idLabel = Label(data_frame,text="Id")
		idLabel.grid(row=0,column=1,padx=5,pady=10)
		f_name_label = Label(data_frame,text="Nom")
		f_name_label.grid(row=0,column=2,padx=5,pady=10)
		l_name_label = Label(data_frame,text="Prénom")
		l_name_label.grid(row=0,column=3,padx=1,pady=10)
		date_label = Label(data_frame,text="Date de naissance")
		date_label.grid(row=0,column=4,padx=1,pady=10)
		gender_labelH = Label(data_frame,text="Sexe")
		gender_labelH.grid(row=0,column=5,padx=20,pady=10)
		gender_labelF = Label(data_frame,text="")
		gender_labelF.grid(row=0,column=6,padx=0,pady=10)
		class_label = Label(data_frame,text="Elo")
		class_label.grid(row=0,column=7,padx=5,pady=10)
		 

		# Logical Entry boxes
		idSpinBox = Spinbox(data_frame,from_=1,to=20,font=("helvetica",10),width=2)
		idSpinBox.grid(row=1,column=1,padx=10,pady=10)
		f_nameBox = Entry(data_frame,width=25)
		f_nameBox.grid(row=1,column=2,padx=10,pady=10)
		l_nameBox = Entry(data_frame,width=25)
		l_nameBox.grid(row=1,column=3,padx=10,pady=10)
		date_Box = DateEntry(data_frame,width=15,locale='fr_FR',selectmode='day',date_pattern='dd/MM/yyyy')
		date_Box.delete(0,END)
		date_Box.grid(row=1,column=4,padx=1,pady=10)
		gender = StringVar()
		gender.set(None)
		gender_BoxH = Radiobutton(data_frame,text="H",variable=gender,value="Homme",width=2)
		gender_BoxH.grid(row=1,column=5,padx=0,pady=10)
		gender_BoxF = Radiobutton(data_frame,text="F",variable=gender,value="Femme",width=2)
		gender_BoxF.grid(row=1,column=6,padx=0,pady=10)
		class_spinBox = Spinbox(data_frame,from_=0,to=50,font=("helvetica",10),width=2)
		class_spinBox.grid(row=1,column=7,padx=10,pady=10)

		# ================Button Commands(rm = remove)======================
		button_frame = LabelFrame(playerFrame,text="Commandes")
		button_frame.pack(fill="x",padx=70,pady=20)

		add_button = Button(button_frame,text="Ajouter",command=add_Entries)
		add_button.grid(row=0,column=0,padx=10,pady=20)

		modif_button = Button(button_frame,text="Modifier",command=update_one_record) 
		modif_button.grid(row=0,column=1,padx=10,pady=20)

		rm_one_button = Button(button_frame,text="Supprimer",command=remove_one_record)
		rm_one_button.grid(row=0,column=2,padx=10,pady=20)

		rm_all_button = Button(button_frame,text="Supprimer tout",command=remove_all_Records)
		rm_all_button.grid(row=0,column=3,padx=10,pady=20)

		clear_button = Button(button_frame,text="Clear",command=clear_Entries)
		clear_button.grid(row=0,column=5,padx=10,pady=20)

		quit_button = Button(button_frame,text="Quitter",command=quitPlayerWindow)#self.quitPlayerView())
		quit_button.grid(row=0,column=7,padx=10,pady=20)

		# Bind the treeview
		tree_frame.bind("<ButtonRelease-1>",selectEntry)

		#createTable()
		query_database()
		


		
	
	

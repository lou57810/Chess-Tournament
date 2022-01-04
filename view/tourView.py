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



class TourWindow:
	def __init__(self):		
		pass
	
	def tourView(self,tourFrame):
		# Create a Treeview Frame		
		tourFrame.pack(pady=20)		
		tree_frame = ttk.Treeview(tourFrame)
		
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
		tree_scroll = Scrollbar(tourFrame)
		tree_scroll.pack(side=RIGHT,fill=Y)

		# Configure the Scrollbar
		tree_frame = ttk.Treeview(tourFrame,yscrollcommand=tree_scroll.set,select="extended")
		tree_frame.pack(pady=20)
		tree_scroll.config(command=tree_frame.yview)

		# Define Columns
		tree_frame["columns"] = ("turn_name","place_name","start_date","end_date","turn_count","timing","description")

		# Create Striped Row Tags
		tree_frame.tag_configure('oddrow',background="white")
		tree_frame.tag_configure('evenrow',background="lightblue")

		# ==========================Database============================
		serialized_turns = {}

		db = TinyDB('data/db_tournaments.json')	
		tournaments_table = db.table('tournaments')

		# ============================Fcts===============================
		def add_Entries():		
			global count	
			
			# Output to entry boxes
			count = len(tree_frame.get_children())
			
			if count % 2 == 0:
				tree_frame.insert(parent="",index=count,iid=count,text="",values=(
					nameBox.get(),
					placeBox.get(),
					startDateBox.get(),
					endDateBox.get(),
					count_spinBox.get(),
					time_shot.get(),			
					descriptBox.get()),
					tags=('evenrow',)
					)
			else:
				tree_frame.insert(parent="",index=count,iid=count,text="",values=(			
					nameBox.get(),
					placeBox.get(),
					startDateBox.get(),
					endDateBox.get(),
					count_spinBox.get(),
					time_shot.get(),			
					descriptBox.get()),
					tags=('oddrow',)
					)
			count +=1
			
			register_Datas()	# Filling DB	
			clear_Entries()

		# Update records: delete all & rewrite ?
		def update_one_record():
			x = tree_frame.selection()[0]	
			records = tournaments_table.all()
			
			tournaments_table.insert({									
					'turn_name': nameBox.get(),
					'place_name': placeBox.get(),			
					'start_date': startDateBox.get(),
					'end_date': endDateBox.get(),
					'turn_count': count_spinBox.get(),
					'timing': time_shot.get(),
					'description': descriptBox.get()
					})

			el = tournaments_table.all()[int(x)]		
			tournaments_table.remove(doc_ids=[el.doc_id])

			# refresh my_tree
			tree_frame.delete(x)
			if count % 2 == 0:
				tree_frame.insert(parent="",index=count,iid=count,text="",values=(
					nameBox.get(),
					placeBox.get(),
					startDateBox.get(),
					endDateBox.get(),
					count_spinBox.get(),
					time_shot.get(),			
					descriptBox.get()),
					tags=('evenrow',)
					)
			else:
				tree_frame.insert(parent="",index=count,iid=count,text="",values=(			
					nameBox.get(),
					placeBox.get(),
					startDateBox.get(),
					endDateBox.get(),
					count_spinBox.get(),
					time_shot.get(),			
					descriptBox.get()),
					tags=('oddrow',)
					)

		def remove_One_Entry():
			#clear_Entries()
			x = my_tree.selection()[0]	
			tree_frame.delete(x)	
			
			tournaments_table = db.table('tournaments')		
			el = tournaments_table.all()[int(x)]		
			tournaments_table.remove(doc_ids=[el.doc_id])
			messagebox.showinfo("Deleted!", "Your record is deleted")
			clear_Entries()

		def remove_all_Records():
			response = messagebox.askyesno("Cette opératon est irréversible!!")	
			tournaments_table = db.table('tournaments')
			if response == 1:
				# Clear the treeview
				for record in my_tree.get_children():
					tree_frame.delete(record)
				tournaments_table.truncate()

		def register_Datas():	
			tournaments_table = db.table('tournaments')	
			tournaments_table.insert({									
					'turn_name': nameBox.get(),
					'place_name': placeBox.get(),			
					'start_date': startDateBox.get(),
					'end_date': endDateBox.get(),
					'turn_count': count_spinBox.get(),
					'timing': time_shot.get(),
					'description': descriptBox.get()
					})


		def clear_Entries():			
			nameBox.delete(0,END)
			placeBox.delete(0,END)	
			startDateBox.delete(0,END)
			endDateBox.delete(0,END)
			count_spinBox.delete(0,END)	
			time_shot.set(None)		# gender.deselect() don't work		
			descriptBox.delete(0,END)

		# Selection curseur souris
		def selectEntry(e):	
			clear_Entries()
			
			# Grab record Number
			selected = tree_frame.focus()

			# Grab record values
			values = tree_frame.item(selected,'values')
			nameBox.insert(0,values[0])
			placeBox.insert(0,values[1])	
			startDateBox.insert(0,values[2])
			endDateBox.insert(0,values[3])
			count_spinBox.insert(0,values[4])

			# ==========RadioBtn===========
			if values[5] == "bullet":		
				bulletRadio.invoke()		
			elif values[5] == "blitz":		
				blitzRadio.invoke()
			elif values[5] == "rapide":
				fastRadio.invoke()
			# =============================
			
			descriptBox.insert(0,values[6])

		def query_database():	
			global count
			count = 0	
			tournaments_table = db.table('tournaments')	
			records = tournaments_table.all()

			n = 0	
			for record in records:
				if n % 2 == 0:		
					tree_frame.insert(parent="",index=n,iid=n,text='',
						values=(								
						records[n]['turn_name'],
						records[n]['place_name'],
						records[n]['start_date'],
						records[n]['end_date'],
						records[n]['turn_count'],
						records[n]['timing'],
						records[n]['description']),
					tags=('evenrow',))
			
				else:
					tree_frame.insert(parent="",index=n,iid=n,text='',
						values=(				
						records[n]['turn_name'],
						records[n]['place_name'],
						records[n]['start_date'],
						records[n]['end_date'],
						records[n]['turn_count'],
						records[n]['timing'],
						records[n]['description']),				
					tags=('oddrow',))
				n += 1

		def quitTournamentWindow(self):			
			tournament_frame.destroy()


		
		# ==============================Fill the Treeview============================
		#display_dataPlayers()
		# Format columns
		tree_frame.column("#0",width=0,stretch=NO)
		tree_frame.column("turn_name",anchor=W,width=130)
		tree_frame.column("place_name",anchor=W,width=130)
		tree_frame.column("start_date",anchor=CENTER,width=130)
		tree_frame.column("end_date",anchor=CENTER,width=130)
		tree_frame.column("turn_count",anchor=CENTER,width=120)
		tree_frame.column("timing",anchor=CENTER,width=130)
		tree_frame.column("description",anchor=CENTER,width=130)

		# Create headings
		tree_frame.heading("#0",text="",anchor=W)
		tree_frame.heading("turn_name",text="Nom du tournoi",anchor=CENTER)
		tree_frame.heading("place_name",text="Lieu",anchor=W)
		tree_frame.heading("start_date",text="Date début",anchor=W)
		tree_frame.heading("end_date",text="Date fin",anchor=W)
		tree_frame.heading("turn_count",text="Nombre de tours",anchor=CENTER)
		tree_frame.heading("timing",text="Choix du temps",anchor=CENTER)
		tree_frame.heading("description",text="Description",anchor=CENTER)

		# ================Add Management Entries Boxes=================
		data_frame = LabelFrame(tourFrame,text="Management Tournois")
		data_frame.pack(fill="x",padx=30,pady=20)

		# Labels
		name_label = Label(data_frame,text="Nom")
		name_label.grid(row=0,column=1,padx=45,pady=10)
		place_label = Label(data_frame,text="Lieu")
		place_label.grid(row=0,column=2,padx=60,pady=10)
		startDate_label = Label(data_frame,text="Date début")
		startDate_label.grid(row=0,column=3,padx=40,pady=10)
		endDate_label = Label(data_frame,text="Date Fin")
		endDate_label.grid(row=0,column=4,padx=40,pady=10)
		count_label = Label(data_frame,text="Nombre de tours")
		count_label.grid(row=0,column=5,padx=10,pady=10)
		descript_label = Label(data_frame,text="Description")
		descript_label.grid(row=0,column=6,padx=5,pady=10)

		# Logical Entry boxes
		nameBox = Entry(data_frame,width=25)
		nameBox.grid(row=1,column=1,padx=10,pady=10)
		placeBox = Entry(data_frame,width=25)
		placeBox.grid(row=1,column=2,padx=10,pady=10)
		startDateBox = DateEntry(data_frame,width=15)
		startDateBox.delete(0,END)
		startDateBox.grid(row=1,column=3,padx=1,pady=10)
		endDateBox = DateEntry(data_frame,width=15)
		endDateBox.delete(0,END)
		endDateBox.grid(row=1,column=4,padx=1,pady=10)
		count_spinBox = Spinbox(data_frame,from_=0,to=100,font=("helvetica",10),width=2)
		count_spinBox.grid(row=1,column=5,padx=5,pady=10)
		descriptBox = Entry(data_frame,width=25)
		descriptBox.grid(row=1,column=6,padx=10,pady=10)

		# RadioButtons
		time_shot = StringVar()
		time_shot.set(None)

		

		radio_frame = LabelFrame(tourFrame,text="Choix du temps")
		
		bulletRadio = Radiobutton(radio_frame,text="Bullet",variable=time_shot,value="bullet",width=10)
		fastRadio = Radiobutton(radio_frame,text="Rapide",variable=time_shot,value="rapide",width=10)
		blitzRadio = Radiobutton(radio_frame,text="Blitz",variable=time_shot,value="blitz",width=10)
		bulletRadio.grid(row=1,column=0,padx=30)
		fastRadio.grid(row=1,column=1,padx=30)
		blitzRadio.grid(row=1,column=2,padx=30)

		radio_frame.pack()

		# ================Button Commands(rm = remove)======================
		button_frame = LabelFrame(tourFrame,text="Commandes")
		#button_frame.pack(fill="x",padx=50,pady=20)
		button_frame.pack(pady=20)

		add_button = Button(button_frame,text="Ajouter",command=add_Entries)
		add_button.grid(row=0,column=0,padx=10,pady=20)

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

		query_database()
		
	

	
	
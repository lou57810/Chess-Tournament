from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import PIL
from PIL import ImageTk,Image
from tkinter import messagebox
from tkcalendar import *
#import sqlite3
from tinydb import TinyDB, Query,where
from tinydb.operations import delete

class PlayerManager:
	def __init__(self,root):
		self.root = root		
		#self.playerFrameManager()

	def playerFrameManager(self):

		# Create a Treeview Frame
		frame = Frame(self.root)
		frame.pack(pady=20)

		tree_frame = ttk.Treeview(frame)


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
		tree_scroll = Scrollbar(frame)
		tree_scroll.pack(side=RIGHT,fill=Y)

		# Configure the Scrollbar
		tree_frame = ttk.Treeview(frame,yscrollcommand=tree_scroll.set,select="extended")
		tree_frame.pack(pady=20)
		tree_scroll.config(command=tree_frame.yview)

		# Define Columns
		tree_frame["columns"] = ("first_name","last_name","birth_date","gender","classement")

		# Create Striped Row Tags
		tree_frame.tag_configure('oddrow',background="white")
		tree_frame.tag_configure('evenrow',background="lightblue")

		# ==========================Database============================
		serialized_player = {}

		db = TinyDB('data/db_player.json')	
		players_table = db.table('players')

		# ===========================Fcts ==============================

		def add_Entries():		
			global count	
			
			# Output to entry boxes
			count = len(tree_frame.get_children())
			
			if count % 2 == 0:
				tree_frame.insert(parent="",index=count,iid=count,text="",values=(						
					f_nameBox.get(),
					l_nameBox.get(),			
					date_Box.get_date(),
					gender.get(),				
					class_spinBox.get()),
					tags=('evenrow',)
					)

			else:
				tree_frame.insert(parent="",index=count,iid=count,text="",values=(			
					f_nameBox.get(),
					l_nameBox.get(),			
					date_Box.get_date(),
					gender.get(),				
					class_spinBox.get()),
					tags=('oddrow',)
						)
			count +=1
			
			register_Datas()	# Filling DB	
			clear_Entries()
			
		def register_Datas():	
			players_table = db.table('players')	
			players_table.insert({									
					'first_name': f_nameBox.get(),
					'last_name': l_nameBox.get(),			
					'birth_date': date_Box.get(),
					'gender': gender.get(),
					'classement': class_spinBox.get()
					})	

		def query_database():	
			global count
			count = 0	
			players_table = db.table('players')	
			records = players_table.all()

			n = 0	
			for record in records:
				if n % 2 == 0:		
					tree_frame.insert(parent="",index=n,iid=n,text='',
						values=(								
						records[n]['first_name'],
						records[n]['last_name'],
						records[n]['birth_date'],
						records[n]['gender'],
						records[n]['classement']),
					tags=('evenrow',))
					
				else:
					tree_frame.insert(parent="",index=n,iid=n,text='',
						values=(				
						records[n]['first_name'],
						records[n]['last_name'],
						records[n]['birth_date'],
						records[n]['gender'],
						records[n]['classement']),				
					tags=('oddrow',))
				n += 1
			
		def remove_One_Entry():
			#clear_Entries()
			x = tree_frame.selection()[0]	
			tree_frame.delete(x)	
			
			players_table = db.table('players')		
			el = players_table.all()[int(x)]		
			players_table.remove(doc_ids=[el.doc_id])
			messagebox.showinfo("Deleted!", "Your record is deleted")
			clear_Entries()

		def remove_all_Records():
			response = messagebox.askyesno("Cette opératon est irréversible!!")	
			players_table = db.table('players')
			if response == 1:
				# Clear the treeview
				for record in my_tree.get_children():
					tree_frame.delete(record)
				players_table.truncate()	

		def clear_Entries():			
			f_nameBox.delete(0,END)
			l_nameBox.delete(0,END)	
			date_Box.delete(0,END)	
			gender.set(None)	# gender.deselect() don't work		
			class_spinBox.delete(0,END)
			
		# Update records: delete all & rewrite ?
		def update_one_record():
			x = tree_frame.selection()[0]	
			records = players_table.all()
			#n = len(players_table)
			
			players_table.insert({									
					'first_name': f_nameBox.get(),
					'last_name': l_nameBox.get(),			
					'birth_date': date_Box.get(),
					'gender': gender.get(),
					'classement': class_spinBox.get()
					})

			el = players_table.all()[int(x)]		
			players_table.remove(doc_ids=[el.doc_id])

			# refresh my_tree
			tree_frame.delete(x)
			if count % 2 == 0:
				tree_frame.insert(parent="",index=x,iid=x,text="",values=(						
					f_nameBox.get(),
					l_nameBox.get(),			
					date_Box.get_date(),
					gender.get(),				
					class_spinBox.get()),
					tags=('evenrow',)
					)

			else:
				tree_frame.insert(parent="",index=x,iid=x,text="",values=(			
					f_nameBox.get(),
					l_nameBox.get(),			
					date_Box.get_date(),
					gender.get(),				
					class_spinBox.get()),
					tags=('oddrow',)
					)
			
		# Selection curseur souris
		def selectEntry(e):	
			clear_Entries()
			
			# Grab record Number
			selected = tree_frame.focus()

			# Grab record values
			values = tree_frame.item(selected,'values')
					
			f_nameBox.insert(0,values[0])
			l_nameBox.insert(0,values[1])	
			date_Box.insert(0,values[2])

			# ==========RadioBtn===========
			if values[3] == "Homme":		
				gender_BoxH.invoke()
				
			elif values[3] == "Femme":		
				gender_BoxF.invoke()
			# =============================
			
			class_spinBox.insert(0,values[4])

		def cleanWindow():			
			frame.destroy()

		# =====================Fill the Treeview======================
		#def displayPlayers()

		#display_dataPlayers()
		# Format columns
		tree_frame.column("#0",width=0,stretch=NO)
		tree_frame.column("first_name",anchor=W,width=130)
		tree_frame.column("last_name",anchor=W,width=130)
		tree_frame.column("birth_date",anchor=CENTER,width=130)
		tree_frame.column("gender",anchor=CENTER,width=120)
		tree_frame.column("classement",anchor=CENTER,width=130)

		# Create headings
		tree_frame.heading("#0",text="",anchor=W)	
		tree_frame.heading("first_name",text="Nom",anchor=W)
		tree_frame.heading("last_name",text="Prénom",anchor=W)
		tree_frame.heading("birth_date",text="Date de naissance",anchor=CENTER)
		tree_frame.heading("gender",text="Sexe H/F",anchor=CENTER)
		tree_frame.heading("classement",text="Classement",anchor=CENTER)

		# ================Add Management Entries Boxes=================
		data_frame = LabelFrame(frame,text="Management Joueurs")
		data_frame.pack(fill="x",padx=70)

		# Labels
		f_name_label = Label(data_frame,text="Nom")
		f_name_label.grid(row=0,column=1,padx=5,pady=10)
		l_name_label = Label(data_frame,text="Prénom")
		l_name_label.grid(row=0,column=2,padx=1,pady=10)
		date_label = Label(data_frame,text="Date de naissance")
		date_label.grid(row=0,column=3,padx=1,pady=10)
		gender_labelH = Label(data_frame,text="Sexe")
		gender_labelH.grid(row=0,column=4,padx=20,pady=10)
		gender_labelF = Label(data_frame,text="")
		gender_labelF.grid(row=0,column=5,padx=0,pady=10)
		class_label = Label(data_frame,text="Classement")
		class_label.grid(row=0,column=6,padx=5,pady=10)
		 

		# Logical Entry boxes
		f_nameBox = Entry(data_frame,width=25)
		f_nameBox.grid(row=1,column=1,padx=10,pady=10)
		l_nameBox = Entry(data_frame,width=25)
		l_nameBox.grid(row=1,column=2,padx=10,pady=10)
		date_Box = DateEntry(data_frame,width=15)
		date_Box.delete(0,END)
		date_Box.grid(row=1,column=3,padx=1,pady=10)
		gender = StringVar()
		gender.set(None)
		gender_BoxH = Radiobutton(data_frame,text="H",variable=gender,value="Homme",width=2)
		gender_BoxH.grid(row=1,column=4,padx=0,pady=10)
		gender_BoxF = Radiobutton(data_frame,text="F",variable=gender,value="Femme",width=2)
		gender_BoxF.grid(row=1,column=5,padx=0,pady=10)
		class_spinBox = Spinbox(data_frame,from_=0,to=50,font=("helvetica",10),width=2)
		class_spinBox.grid(row=1,column=6,padx=10,pady=10)

		# ================Button Commands(rm = remove)======================
		button_frame = LabelFrame(frame,text="Commandes")
		button_frame.pack(fill="x",padx=70,pady=20)

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

		record_button = Button(button_frame,text="Quitter",command=cleanWindow)
		record_button.grid(row=0,column=7,padx=10,pady=20)

		# Bind the treeview
		tree_frame.bind("<ButtonRelease-1>",selectEntry)

		#createTable()
		query_database()

		self.root.mainloop()


import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
import os
import time
import shutil
#from .mainWindow import Window

class Screen():
	def __init__(self):						    # Constructeur init attribs & methodes
		self.root = Tk()
		self.root.geometry("1024x760+400+100")
		#self.root.wm_overrideredirect(True)		# Cache la barre de titre		
		
		# Add Frame
		self.main_frame = Frame(self.root, bg='dark red')
		self.main_frame.pack(fill="both",expand=True)
		# Add Text
		label_title = Label(self.main_frame, text="Welcome to International Chess Game", font=("Arial", 20), bg='dark red', fg ='white')
		label_title.place(x=280, y=50)
		
		# Fenêtre image gif
		self.image_label = Label(self.main_frame,image="")		
		self.image_label.place(x=(1024/2 - 768/2), y=150)
		self.dirPath = 'gif_frames'
		os.mkdir(self.dirPath)	# Dossier temporaire
		self.shutil =shutil
		self.start = time.time()

		self.gif_frames = []
		self.images = []
		self.animation()
		
		self.root.mainloop()

	def animation(self):
		gif = Image.open('./img/eChess.gif')				# Ouvre eChess.gif
		self.no_of_frames = gif.n_frames

		for i in range(self.no_of_frames):					# img gif de 0 à 36 
			gif.seek(i)
			gif.save(os.path.join('gif_frames',f'gif{i}.png'))	# path img
			self.gif_frames.append(os.path.join('gif_frames', f'gif{i}.png'))	# remplissage de gif_frames

		for images in self.gif_frames:
			im = Image.open(images)
			im = im.resize((768,432),Image.ANTIALIAS)	# resizing au cas ou !
			im = ImageTk.PhotoImage(im)					# tk crée des objets images
			self.images.append(im)						# remplissage 'images'

		self.show_animation(0)							# on passe la première image à la fct

	def show_animation(self,count):

		image = self.images[count]
		self.image_label.configure(image=image)			# affichage label 1 par 1
		count += 1
		if count == len(self.images)-1:					# fin de la boucle
			count = 0
		if int(time.time()-self.start) != 5:
			self.x = self.root.after(80,self.show_animation,count)
		else:
			self.root.after_cancel(self.x)
			self.splashEnd(self.main_frame)				# appel splashEnd depuis mainWindow.py			
			#self.shutil.rmtree(self.dirPath)			# Supprime les fichiers et le rep (à utiliser avec try except)

	def splashEnd(self, f):
		self.main_frame.pack_forget()
		self.root.destroy()		
		self.root.mainloop()
		self.shutil.rmtree(self.dirPath)

		
	"""	

	def mainMenuWindow(self,f):
		self.main_frame.pack_forget()
		#self.first = Frame(self.root,background = "grey")
		
		#self.first.pack(fill="both",expand=True)
	"""

		#Label(self.first,text="First Page",font="lucida 20 bold").place(x=40,y=20)

#Screen()






import tkinter as tk
from tkinter import *
from tkinter import ttk
import time

class Controller:
	def __init__(self):
		pass

	def getTime():			
		date = time.strftime('%d/%m/%y %H:%M:%S',time.localtime())
		return date
		 
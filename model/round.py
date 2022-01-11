from tinydb import TinyDB, Query, where
#import data	# db_tournaments.json
from model.player import Player
from tinydb.operations import set
import copy

class Round:
	def __init__(self,matchName,playerName,score,startTime,endTime):		 
		self.matchName 		= matchName
		self.playerName		= playerName
		self.score 			= score		
		self.startTime 		= startTime
		self.endTime 		= endTime

		self.upperList = []
		self.lowerList = []

	def initFirstRound():
		# ==========================Database============================		
		"""
		serialized_round = {
							'matchName':	getName.matchName,
							'playerName':	getPlayerName().playerName,
							'score':		getScore.startTime,
							'startTime':	getTime().startTime,							
							'endTime':		getTime().endTime
							}
		"""
		pass

	def getPlayerDatas():				
		db = TinyDB('data/db_tournaments.json')		
		round_table = db.table('round')
		serialized_rounds = round_table.all()
		
		
		tupleList = list()
		binome = ()		# Tuple				
		i = 0
		
		query0 = 'first_name'
		query1 = 'last_name'
		query2 = 'rank'
		while i < len(serialized_rounds):
			binome =(serialized_rounds[i].get(query0)+" "+serialized_rounds[i].get(query1), int(serialized_rounds[i].get(query2)))			
			tupleList.insert(i,binome)						
			i += 1
		# Sort(tupleList)
		tupleList.sort(key = lambda x: x[1])   #index 2 means third element
		# Fraction in two lists
		n = 4
		lower_upperList = [tupleList[i:i + n] for i in range(0, len(tupleList), n)]
		print(lower_upperList)

		
		

		
		



		


			

			

			

				

		
		

	

		




		

		








 

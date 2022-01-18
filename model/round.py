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
		self.serialized_rounds = {
							'matchName':	getName.matchName,
							'playerName':	getPlayerName().playerName,
							'score':		getScore.startTime,
							'startTime':	getTime().startTime,							
							'endTime':		getTime().endTime
							} 
		self.tupleList = list()
		self.upperTupleList = list()
		self.lowerTupleList = list()

	def initFirstRound():
		# ==========================Database============================		
		"""
		serialized_rounds = {
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
		round_table = db.table('rounds')
		serialized_rounds = round_table.all()

		tupleList = list()
		

		binome = ()		# Tuple				
		i = 0
		query0 = 'id'			# elt0
		query1 = 'first_name'	#{elt1,								
		query2 = 'last_name'	# elt1}
		query3 = 'rank'			# elt2
		while i < len(serialized_rounds):
			binome =(int(serialized_rounds[i].get(query0)),serialized_rounds[i].get(query1)+" "+serialized_rounds[i].get(query2), int(serialized_rounds[i].get(query3)))			
			tupleList.insert(i,binome)						
			i += 1
		# Sort(tupleList)
		tupleList.sort(key = lambda x: x[2])   #index 2 means third element
		#print(tupleList)
		# Fraction in two lists
		#print("tupleList[0]: ",tupleList[0][2])

		return tupleList
		
		

			

		
		

		
		

		
		



		


			

			

			

				

		
		

	

		




		

		








 

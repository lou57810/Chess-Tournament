from model.player import Player
from tinydb import TinyDB


class PlayerController:
	
	def __init__(self,root):
		"""
		for elt in args:
            self.id         = elt[0]
            self.first_name = elt[1]
            self.last_name  = elt[2]
            self.birth_date = elt[3]
            self.gender     = elt[4]
            self.rank       = elt[5]
            self.score      = elt[6]
		"""
		pass



	def createPlayer(self):
		data = []
		data_check = TRUE
		player = Player(data)


	def register_dataOnePlayer(self):
		"""	
		data = []
		data_check = TRUE
        for element in input_list:
            # Get all input
            data.append(element.get())
            # Check if field is empty or not
            if not element.get():
                data_check = FALSE
		player = Player(data)		
		#player = Player(id='',first_name='',last_name='',birth_date='',gender='',rank='',score='')

		print("self.player.id:",self.player.id)# = idSpinBox.get()
																				
		player.first_name = f_nameBox.get(),
		player.last_name = l_nameBox.get(),			
		player.birth_date = date_Box.get(),
		player.gender = gender.get(),
		player.rank = class_spinBox.get(),
		player.score = 0
		"""
		pass

	def register_one_playerSet(self, s):
			db = TinyDB('data/db_tournaments.json')	
			players_table = db.table('players')
			players_table.insert(s)
			"""
			for elt in playerDatas:
				players_table.insert({
					'id': elt['id'],														
					'first_name': elt['first_name'],
					'last_name': elt['last_name'],			
					'birth_date': elt['birth_date'],
					'gender': elt['gender'],
					'rank': elt['rank'],
					'score': 0
					})			

			print("playerList :", playerList[0], playerList[0]['id'])
			
			"""

	def register_all_playersSetTest():
		db = TinyDB('data/db_tournaments.json')	
		players_table = db.table('players')
		"""
		for elt in playerDatas:
						players_table.insert({
							'id': elt['id'],														
							'first_name': elt['first_name'],
							'last_name': elt['last_name'],			
							'birth_date': elt['birth_date'],
							'gender': elt['gender'],
							'rank': elt['rank'],
							'score': 0
							})			

		print("playerList :", playerList[0], playerList[0]['id'])
		"""

		serialized_players = {}
		playerList = list()
			
		for row_id in tree_frame.get_children():				
			serialized_players = {
										'id': tree_frame.set(row_id,0),
										'first_name': tree_frame.set(row_id,1),
										'last_name': tree_frame.set(row_id,2),
										'birth_date': tree_frame.set(row_id,3),
										'gender': tree_frame.set(row_id,4),
										'rank': tree_frame.set(row_id,5),
										'score': '0'
										}
			playerList.append(serialized_players)
				#players_table.truncate()
				#players_table.insert_multiple(serialized_players)


			print("PList: ",playerList)

		


		
	
	
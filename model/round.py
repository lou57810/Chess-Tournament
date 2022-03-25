from tinydb import TinyDB, Query, where
# import data	# db_tournaments.json
from model.player import Player
# from model.tournament import Tournaments
from tinydb.operations import set
import copy



class Round:
    def __init__(self,name,start_time,round_list,end_time):
        self.name = name
        self.start_time = start_time
        self.round_list = round_list
        self.end_time = end_time



    def initFirstRound(self):
        pass
        """
        db = TinyDB('data/db_tournaments.json')
        players_table = db.table('players')

        serialized_players = players_table.all()
        serialized_players.sort(key=operator.itemgetter('rank'), reverse=True)  # Tri suivant le classement
        firstRoundList = list()

        i = 0
        playerSet = list()
        challengers = list()

        while i < len(serialized_players):  # Liste comprenant [id,(nom et prénom),rang] ===> treeview
            challengers = [serialized_players[i].get('id'),
                           (serialized_players[i].get('first_name') + " " + serialized_players[i].get('last_name')),
                           serialized_players[i].get('rank')]

            # challengers = [serialized_players[i].get('id'), serialized_players[i].get('score')]
            firstRoundList.insert(i, challengers)  # Insertion challengers à l'indice i
            i += 1
        #print(firstRoundList)
        return firstRoundList

    

    def initSecondRound(self):
        db = TinyDB('data/db_tournaments.json')
        # round_table = db.table('rounds')
        players_table = db.table('players')
        orderedList = Round.getScores()
        id = orderedList[0][0]
        # print("id:",id)
        User = Query()
        tempList = list()
        challengers = list()
        i = 0
        while i < len(orderedList):
            # print("i:",i)
            # print("idListi : ",orderedList[i][0])
            l = orderedList[i][0]
            tempList.append(players_table.search(User.id == l))
            # print("1:",players_table.search(User.id==l))
            # print("tmp: ",tempList[i])
            i += 1
        i = 0
        secondList = list()
        serialized_players = players_table.all()
        # serialized_players.sort(key=operator.itemgetter('rank'),reverse=True)  # Tri suivant le classement
        while i < len(serialized_players):  # Liste comprenant [id,(nom et prénom),rang] ===> treeview
            challengers = ([serialized_players[i].get('id'),
                            (serialized_players[i].get('first_name') + " " + serialized_players[i].get('last_name')),
                            serialized_players[i].get('rank'), serialized_players[i].get('score')])
            secondList.insert(i, challengers)
            i += 1

        score1List = list()
        score05List = list()
        score0List = list()
        i = 0

        # for elt in secondList:
        while i < len(secondList):
            for elt in secondList:
                if elt[3] == '1':
                    score1List.append(elt)
                    score1List.sort(key=lambda x: x[2], reverse=True)
                elif elt[3] == '0.5':
                    score05List.append(elt)
                    score05List.sort(key=lambda x: x[2], reverse=True)
                elif elt[3] == '0':
                    score0List.append(elt)
                    score0List.sort(key=lambda x: x[2], reverse=True)
                i += 1

        secondRoundList = list()
        secondRoundList = score1List + score05List + score0List
        # print("secondRoundList: ",secondRoundList)
        return secondRoundList

    
    def regDbMatch(self, match, x):
        db = TinyDB('data/db_tournaments.json')
        tournament_round_list = list()
        rounds_list = list()
        players_table = db.table('players')
        tournaments_table = db.table('tournaments')

        # Match = tuple de deux listes : ([Joueur1,score],[Joueur2,score])
        # Matchs multiples = liste sur l'instance du tour: {Round1{1,{[(m1),(m2),(m3),(m4)] },{}...

        User = Query()
        players_table.update({'score': match[0][1]}, User.id == match[0][0])  # Mise à jour db score joueur 1
        players_table.update({'score': match[1][1]}, User.id == match[1][0])  # Mise à jour db score joueur 2

        x = int(x) + 1  # n° ligne et de match
        x = str(x)
        # roundList = match
        #rounds_list = match
        # roundMatchList

        rounds_list.append({'match' + x: match})  # db: insert({'match + n°', tuple(id,score)})
        # tournament_round_list.append(round_list)
        # return tournament_round_list
        self.roundMatchList = rounds_list
        #print("round_list: ",rounds_list)
        #User = Query()
        #tournaments_table.search(where(User.place_name == 'London'))
        #tournaments_table.insert({'roundMatchList': self.roundMatchList})

        # Tournaments.regTournament(round)
        # return round_list
    """



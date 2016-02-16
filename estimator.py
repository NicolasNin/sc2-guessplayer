import utils
import collections
import math
class PPVEstimator():
	def __init__(self,method="manhattan"):
		""" estimator a la scikit
		but we want to customize a few thing
		in particular the predict we add a predict_verbose
		method which gives the argmax of predict and all other kind of info
		"""
		self.liste_of_games=[]
		self.dictofplayer={}
		#self.liste_of_players=[]
		self.liste=False #do we use a list of game or a dict of player with a list of games
		
	def fit(self,data,liste=True):
		#data are a list of games a la scikit
		#or data might be a dict with key being the players
		print("Fit estimator with data from database")
		self.dictofplayer=data.players
		
		if liste:
			for g in data:
				self.liste_of_games.append(g)
		else:
			for p in data.players:
				for g in data.players[p]:
					self.liste_of_games.append(g)
	def predict(self,game,output="basic",race=True):
		#we give a game and we compare to every game in liste_of_games
		#we return the best match 
		l=[]
		mini=1000000 #lazy way
		raceofplayer=game.race1 
		for g in self.liste_of_games:
			a=self.score(g,game)
			if mini>a:
				mini=a
				game_best=g
		if output=="basic":		
			return game_best.player1
		elif output=="game":
			return game_best
		elif output=="gameandscore":
			return (mini,game) 
	def predictByPlayer(self,game,method="manhattan",option=2,output="basic",race=True):			
		#same as predict but we use the dict the ouput is every score and game
		mini=1000000 #lazy way
		race=game.race1
		for p in self.dictofplayer:
			if self.dictofplayer[p][0].race1==race:
				for g in self.dictofplayer[p]:
					a=self.score(g,game,method,option)
					if mini>a:
						mini=a
						game_best=g
		if output=="basic":		
			return game_best.player1
		elif output=="game":
			return game_best
		elif output=="gameandscore":
			return (mini,game) 
	def giveProba(self,game,method="manhattan",option=2):
		#we calculate the min score for every player of db1 against the replay
		#the result is a sorted by keys distance where key is name and value is score and game 
		distance=collections.OrderedDict()
		for p in self.dictofplayer:
			if self.dictofplayer[p][0].race1==game.race1:
				mini=100000				
				for g in self.dictofplayer [p]:
					a=self.score(g,game,method,option)
					if (a<mini):
						mini=a
						game_best=g
				distance[p]=(mini,g)
	#	valueoftarget=s["game.player1"][0]
		s=collections.OrderedDict(sorted(distance.items(), key=lambda t: t[1]))
		
		l=[]
		for (i,v) in s.items():
			l.append((i,v[0],v[1]))	
		return l
	def score(self,game1,game2,method="manhattan",option=2):
		if method=="manhattan":
			return utils.manhattan(game1.matrix,game2.matrix)
		elif method=="apm":
			s=utils.manhattan(game1.matrix,game2.matrix)
			ecartapm=abs(game1.APM-game2.APM)/min(game1.APM,game2.APM)
			s=s+math.pow(ecartapm,option)
			return s
			

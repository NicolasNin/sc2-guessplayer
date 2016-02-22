
class PPVEstimator():
	def __init__(self,method="manhatan"):
		""" estimator a la scikit
		but we want to customize a few thing
		in particular the predict we add a predict_verbose
		method which gives the argmax of predict and all other kind of info
		"""
		self.liste_of_games=[]
		#self.liste_of_players=[]
		
	def fit(self,data,liste=True):
		#data are a list of games a la scikit
		#or data might be a dict with key being the players
		
		if liste:
			for g in data:
				self.liste_of_games.append(g)
		else:
			for p in data:
				for g in data[p]:
					self.liste_of_games.append(g)
	def predict(self,game):
		#we give a game and we compare to every game in liste_of_games
		#we return the best match 
		l=[]
		mini=1000000 #lazy way 
		game_best=
		for g in self.liste_of_games:
			a=self.score(g,game)
			if mini>a:
				mini=a
				game_best=g
		return [mini,game_best]		
	def score(game1,game2,method="manhatan")):
		if method=="manhatan":
			return utils.manhatan(game1.matrix,game2.matrix)

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
	def predict(self,game,method="manhattan",option=2,output="basic",race=True,maxgap=15,coefMat=1,coefGap=1,coefApm=1,coefFreq=1,coefMat3=0,coefFirst=0):
		#we give a game and we compare to every game in liste_of_games
		#we return the best match 
		l=[]
		mini=1000000 #lazy way
		raceofplayer=game.race1 
		for g in self.liste_of_games:
			a=self.score(g,game,method,option,maxgap,coefMat,coefGap,coefApm,coefFreq,coefMat3,coefFirst)
			if mini>a:
				mini=a
				game_best=g
		if output=="basic":		
			return game_best.player1
		elif output=="game":
			return game_best
		elif output=="gameandscore":
			return (mini,game) 
	def predictByPlayer(self,game,method="manhattan",option=2,maxgap=15,coefMat=1,coefGap=1,coefApm=1,coefFreq=1,output="basic",race=True,coefMat3=0,coefFirst=0):			
		#same as predict but we use the dict the ouput is every score and game
		mini=1000000 #lazy way
		race=game.race1
		for p in self.dictofplayer:
			if self.dictofplayer[p][0].race1==race:
				for g in self.dictofplayer[p]:
					a=self.score(g,game,method,option,maxgap,coefMat,coefGap,coefApm,coefFreq,coefMat3,coefFirst)
					if mini>a:
						mini=a
						game_best=g
		if output=="basic":	
			return game_best.player1
		elif output=="game":
			return game_best
		elif output=="gameandscore":
			return (mini,game) 
	def giveProba(self,game,method="manhattan",option=2,maxgap=15,coefMat=1,coefGap=1,coefApm=1,coefFreq=1,coefMat3=0,coefFirst=0,puissance=1):
		#we calculate the min score for every player of db1 against the replay
		#the result is a sorted by keys distance where key is name and value is score and game 
		distance=collections.OrderedDict()
		for p in self.dictofplayer:
			if self.dictofplayer[p][0].race1==game.race1:
				mini=100000				
				for g in self.dictofplayer [p]:
					a=self.score(g,game,method,option,maxgap,coefMat,coefGap,coefApm,coefFreq,coefMat3,coefFirst,puissance)
					if (a<mini):
						mini=a
						game_best=g
				distance[p]=(mini,game_best)
	#	valueoftarget=s["game.player1"][0]
		s=collections.OrderedDict(sorted(distance.items(), key=lambda t: t[1]))
		
		l=[]
		for (i,v) in s.items():
			l.append((i,v[0],v[1]))	
		return l
		
	def score(self,game1,game2,method="manhattan",option=2,maxgap=15,coefMat=1,coefGap=1,coefApm=1,coefFreq=1,coefMat3=0,coefFirst=0,puissance=1):
		#print("coefs",coefMat,coefGap,coefApm,coefFreq)
		all_features=0
		if coefMat!=0:
			all_features+=coefMat*utils.manhattan(game1.matrix,game2.matrix,2.,puissance)
		if coefGap!=0:
			all_features+=coefGap*utils.distancedict(game1.frequency_of_gap,game2.frequency_of_gap,maxgap)
		if coefApm!=0:	
			all_features+=coefApm*pow((max(game1.APM,game2.APM)/min(game1.APM,game2.APM))-1,option)
		if coefFreq!=0:	
			all_features+=coefFreq*utils.distancearray(game1.frequency_of_hotkeys,game2.frequency_of_hotkeys)
		if coefMat3!=0:
			all_features+=coefMat3*utils.distancearray(game1.matrix3,game2.matrix3)
		if coefFirst!=0:
			f1=game1.frequency_of_hotkeys
			f2=game2.frequency_of_hotkeys
			fi1=game1.firstHotkeys
			fi2=game2.firstHotkeys
			s=0
			for i in range(10):
				if(f1[i]>0.05 and f2[i]>0.05):
					a=max(fi1[i],fi2[i])
					b=min(fi1[i],fi2[i])
					s+=(float(a)/float(b))-1
			all_features+=coefFirst*s			
		return all_features
		if method=="manhattan":
			return utils.manhattan(game1.matrix,game2.matrix)
		elif method=="apm":
			s=utils.manhattan(game1.matrix,game2.matrix)
			ecartapm=(max(game1.APM,game2.APM)/min(game1.APM,game2.APM))-1
			s=s+math.pow(ecartapm,option)
			return s
		elif method=="frequency":
			ecartapm=abs(max(game1.APM,game2.APM))/min(game1.APM,game2.APM)-1
			return utils.distancearray(game1.frequency_of_hotkeys,game2.frequency_of_hotkeys)+math.pow(ecartapm,option)
		elif method=="gap":
			s=utils.manhattan(game1.matrix,game2.matrix)
			return utils.distancedict(game1.frequency_of_gap,game2.frequency_of_gap,maxgap)+s
			

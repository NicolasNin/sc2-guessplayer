#sc2-guessplayer
import os
import game
import convert
class dbsc2():
	def __init__(self,name_of_db,limit_matrix=10000,limit_apm=10000):
		self.name=name_of_db
		#storage of games through the name of player1
		#which means that for each replay we have two games
		self.players={}
		self.limit_matrix=limit_matrix
		self.limit_matrix_low=0
		self.limit_apm=limit_apm
		self.normalize=True
		#for scikit to be calculated from self.players when needed
		self.liste_of_player=[] #to be sorted to get classes name in scikit
		#those are (almost)data and target for scikit
		self.liste_games=[]
		self.liste_p1_of_games=[]
		#other data that can be computed
		self.meanAPM={}
######## a few information method
	def isInDb(self,player):
		return (player in self.players.keys())
	def showPlayers(self):
		s=0
		g=0
		for p in self.players:
			print(p +" number of game in db "+ str(len(self.players[p])))
			g+=len(self.players[p])
			s+=1
		print("total number of player " + str(s)+ "total number of games " + str(g))
	def showInfoPlayer(self,player):
		for g in self.players[player]:
			print("{0}({1}) VS {2}({3}) with APM {5} from file {4}".format(g.player1,g.race1,g.player2,g.race2, g.path,g.APM) )
########  method to compute scikit info
	def computeScikit(self):
		self.liste_of_player=[]
		self.liste_games=[]
		self.liste_p1_of_games=[]
		for p in self.players:
			self.liste_of_player.append(p)
			for g in self.players[p]:
				self.liste_games.append(g)
				self.liste_p1_of_games.append(g.player1)

#########  method to update games info such that matrix with the same limit
	def calculateAllMatrix(self,limit=10000,limitlow=0,normalize=True):
		self.limit_matrix=limit
		self.normalize=normalize
		for p in self.players:
			for g in self.players[p]:
				g.calculate_matrix(limit,limitlow)
				if normalize:
					g.normalize_matrix()
	def calculateAllFrequency(self,limit=10000,limitlow=0,normalize=True):
		self.limit_matrix=limit
		for p in self.players:
			for g in self.players[p]:
				g.calculate_frequency(limit,limitlow)
				
	
	def calculateAllAPM(self,limit=10000):
		self.limit_apm=limit
		for p in self.players:
			for g in self.players[p]:
				g.calculateAPMj1(limit)
				
				
	def calculateMeanAPM(self):
		for p in self.players:
			s=0
			i=0
			for g in self.players[p]:
				s+=g.APM
				i+=1
			if (s!=0):
				self.meanAPM[p]=s/i
			else:
				print("no game for player",p)
				self.meanAPM[p]=-1
		#methods to fill this db from directories 
	def addDirectory(self,path):
		#we only add files .SC2Relayp1 and .SC2Relayp2" 
		som=0
		for dirname, dirnames, filenames in os.walk(path):
			for filename in filenames:
				if filename[len(filename)-10:len(filename)]==".SC2Replay":
					som+=1
		print ("adding {0} replay from {1}".format(som,path))	
		
		som2=0
		for dirname, dirnames, filenames in os.walk(path):		
			for filename in filenames:
				if filename[len(filename)-10:len(filename)]==".SC2Replay":
					print("adding",filename,som2+1,"/",som)
					self.addReplay(os.path.join(dirname, filename))
					som2+=1				
	def addReplay(self,path):
		if (os.path.exists(path+"p1") and os.path.exists(path+"p1")):
			g1=self.addReplayFromData(path+"p1")
			g2=self.addReplayFromData(path+"p2")
		else:
			print(path +"not yetconverted")
			(g1,g2)=convert.convertReplay(path)
			if g1!="error":
				g1.calculateAllFeatures(self.limit_matrix,0,self.limit_apm)
				if g1.player1 not in self.players:
					self.players[g1.player1]=[]
				self.players[g1.player1].append(g1)
			if g2!="error":
				g2.calculateAllFeatures(self.limit_matrix,0,self.limit_apm)
				if g2.player1 not in self.players:
					self.players[g2.player1]=[]
				self.players[g2.player1].append(g2)
			return (g1,g2)	
	def addReplayFromData(self,filename):
		#we add the p1 and p2 files
		#print("add "+ filename +"to "+self.name)
		f=open(filename)
		name1=f.readline().rstrip()
		name2=f.readline().rstrip()
		race1=f.readline().rstrip()
		race2=f.readline().rstrip()
		hotkeys=[]
		frames=[]
		for line in f:
			t=line.rstrip().split("\t")
			hotkeys.append(int(t[0]))
			frames.append(int(t[1]))
		#create the game ,verify that list are not empty
		#compute matrix and APM of games 
		if (len(frames)!=0):
			
			g=game.game(name1,name2,race1,race2,hotkeys,frames,path=filename)
			g.calculateAllFeatures(self.limit_matrix,0,self.limit_apm)
			#g.calculate_matrix(self.limit_matrix)
			#g.calculate_frequency(self.limit_matrix)
			#g.calculateFrequencyGap()
			#g.normalize_matrix()
			#g.calculateAPMj1(self.limit_apm)
			
			if g.player1 not in self.players:
				self.players[g.player1]=[]
			self.players[g.player1].append(g)
		else:
			print("empty replay",filename)
		return 	g

##################### TEST #######################
def main():
	print("run test")
	test()
#test path needs to have bad replay
#test path need to have bad p1 or p2 files	
def test():
	testpath="replaytest"
	print ("constructing db from " +testpath)
	db=dbsc2("dbtest")
	db.addDirectory(testpath)
	db.showPlayers()
	db.computeScikit()
	print(db.liste_of_player)
	print(db.liste_games)
	print(db.liste_p1_of_games)
	db.calculateAllMatrix()
	db.calculateMeanAPM()
	db.calculateAllAPM()
	db.calculateAllFrequency()
	print("")
	db.showInfoPlayer("maru")
	print("")
#	print(db.players["maru"][2].matrix)
#	print(db.players["maru"][2].APM)
#	print(db.players["maru"][2].APM)
if __name__ == '__main__':
    main()
    
		
		

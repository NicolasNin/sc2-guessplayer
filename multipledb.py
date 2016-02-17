#sc2-guessplayer
import dbsc2
import estimator
import utils
class multipleDB():
	def __init__(self):
		self.DBs={}
		self.limit_matrix=10000
		self.limit_APM=10000
	def addDb(self,name,path):
		db=dbsc2.dbsc2(name)		
		db.addDirectory(path)	
		self.DBs[name]=db
		self.estimator=estimator.PPVEstimator()
	###method to update all matrix or APM
	def updateAllMatrixAlldb(self,limit=10000,limitlow=0):
		self.limit_matrix=limit 
		for db in self.DBs:
			self.DBs[db].calculateAllMatrix(limit,limitlow)
	
	def updateAllAPMAlldb(self,limit=10000):
		self.limit_APM=limit 
		for db in self.DBs:
			self.DBs[db].calculateAllAPM(limit)
			self.DBs[db].calculateMeanAPM()
	##method to evaluate db against other db using estimator or scikit
	
	def evaluateDB(self,db1,dbtest,method="manhattan",option=2):
		if type(db1)==str:
			db1=self.DBs[db1]
		if type(dbtest)==str:
			dbtest=self.DBs[dbtest]
		#both db are now real db object and not name or number		
		#here we give data as a dict hence the False
		self.estimator.fit(db1,False)
		
		#now we predict for every game in dbtest
		result=[]
		target=[]
		s=0
		for player in dbtest.players:
			if db1.isInDb(player):
				s+=1
				print ("player {0} is being predicted, number {1}".format(player,s))
				for game in dbtest.players[player]:
					result.append(self.estimator.predictByPlayer(game,method,option))
					target.append(game.player1)
		return (result,target)
		
	def scoreEval(self,result,target):
		#result are for now a simple list of name
		#target is also a simple list of name
		s=0
		for i in range(len(result)):
			if result[i]==target[i]:
					s+=1
		print(s)
		return float(s)/len(result)	
	def evaluateProba(self,db1,dbtest,method="manhattan",option=2,fail=False):
		#same as evaluate but now we return the dict of proba by using giveProba which is not a proba but the score min score for each player
		if type(db1)==str:
			db1=self.DBs[db1]
		if type(dbtest)==str:
			dbtest=self.DBs[dbtest]
		self.estimator.fit(db1,False)
		result=[]
		target=[]
		s=0
		for player in dbtest.players:
			isin=db1.isInDb(player)
			if isin or fail:
				s+=1
				str2=""
				if not isin:
					str2="while not in db"
				print (("player {0} is being given probas, number {1}"+str2).format(player,s))
				
				for game in dbtest.players[player]:
					result.append(self.estimator.giveProba(game,method,option))
					target.append(game)
					
		return (result,target)
	def scoreProba(self,resproba,target,threshold=200):
		#resproba is a list of sorted ordered dict with name as key and (value,game) as value
		s=0
		bad_failure=0
		bad_replay=0
		st=0
		sumt=0
		for i in range(len(resproba)):
			
			a=utils.getPosition(target[i].player1,resproba[i])
			if (a==threshold):
				print("{7}:{0}: Guess1 {1} with value {2} |position of {0}: {3} with value {4}|apm of {0}:{5} apm of {1}: {6}".
				format(target[i].player1,
				resproba[i][0][0],
				round(resproba[i][0][1],2),a,
				round(resproba[i][a][1],2),round(target[i].APM,3),round(resproba[i][0][2].APM,3),i))
				st+=1
				sumt+=resproba[i][0][1]
			if (a>0 and threshold==200):
				print("{7}:{0}: Guess1 {1} with value {2} |position of {0}: {3} with value {4}|apm of {0}:{5} apm of {1}: {6}".
				format(target[i].player1,
				resproba[i][0][0],
				round(resproba[i][0][1],2),a,
				round(resproba[i][a][1],2),round(target[i].APM,3),round(resproba[i][0][2].APM,3),i))
				s+=1
				if(a>2):
					bad_failure+=1
				if(resproba[i][0][1]>1):
					bad_replay+=1
		if (st!=0):			
			print("number of position {0}: {1} with mean value {2}".format(threshold,st,round(sumt/st,2)))
		print("Number of games: {0},number of failure {1}({2})% , number of bad failure(>2) {3}({5}%) ,failure not bad {8}, bad replay {4}({6}%) bad failure less bad replay {7}({9}%)| ".format(
		len(target),						
		s,									
		round(float(s)/len(target)*100,3),	
		bad_failure,
		bad_replay,
		round(float(bad_failure)/len(target)*100,2)
		,round(float(bad_replay)/len(target)*100,2)
		,bad_failure-bad_replay		#7
		,s-bad_failure,
		round(float(s-bad_failure)/len(target),2)))
##################### TEST #######################
def main():
	print("run test")
	test()
#test path needs to have bad replay
#test path need to have bad p1 or p2 files	
def test():
	 #test rapide 
	testpath="replaytest/2"
	testpath2="replaytest/1"
	
	#test long
	#testpath="replayofficial/WCS15Season2"
	#testpath2="replayofficial/WCS15Season3"
	m=multipleDB()
	print ("test :addindg two dbs from ")
	m.addDb("1",testpath)
	m.addDb("2",testpath2)
	print("test: updating matrix")
	#m.updateAllMatrixAlldb()
	print("test: updating APM")
	#m.updateAllAPMAlldb()
	print("test: evaluate DB")
	#m.DBs["2"].showPlayers()
	#res,tar=m.evaluateDB("1","2","basic")
	print("test:evaluate Proba")
	res,target=m.evaluateProba("1","2","gap",fail=True)
	m.scoreProba(res,target,-1)
	print("END TEST")
	#print(m.scoreEval(res,tar))
if __name__ == '__main__':
    main()
    		
		

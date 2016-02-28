#sc2-guessplayer
import dbsc2
import estimator
import utils
import math
class multipleDB():
	def __init__(self):
		self.DBs={}
		self.limit_matrix=10000
		self.limit_APM=10000
		self.estimator=estimator.PPVEstimator()
	def addDb(self,name,path):
		db=dbsc2.dbsc2(name)		
		db.addDirectory(path)	
		self.DBs[name]=db
		
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
	
	def evaluateDB(self,db1,dbtest,method="manhattan",option=2,fail=False,maxGap=15,coefMat=1,coefGap=1,coefApm=1,coefFreq=1,coefMat3=0):
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
				#print ("player {0} is being predicted, number {1}".format(player,s))
				for game in dbtest.players[player]:
					result.append(self.estimator.predictByPlayer(game,method,option,maxGap,coefMat,coefGap,coefApm,coefFreq,coefMat3))
					target.append(game.player1)
		return (result,target)
		
	def scoreEval(self,result,target):
		#result are for now a simple list of name
		#target is also a simple list of name
		s=0
		for i in range(len(result)):
			if result[i]==target[i]:
					s+=1
		return float(s)/len(result)	
	def evaluateProba(self,db1,dbtest,method="manhattan",option=2,fail=False,maxGap=15,coefMat=1,coefGap=1,coefApm=1,coefFreq=1,coefMat3=0,puissance=1):
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
					str2=" while not in db"
				print (("player {0} is being given probas, number {1}"+str2).format(player,s))
				
				for game in dbtest.players[player]:
					result.append(self.estimator.giveProba(game,method,option,maxGap,coefMat,coefGap,coefApm,coefFreq,coefMat3,puissance))
					target.append(game)
					
		db1.calculateAC()			
		db1.calculateStatsAc(method="mean")			
		self.scoreProba(result,target,dbtest=db1)			
		return (result,target)
	def scoreProba(self,resproba,target,threshold=200,dbtest=None,treshProba=-100000):
		#resproba is a list of sorted ordered dict with name as key and (value,game) as value
		fail=0
		bad_failure=0
		bad_replay=0
		s=0
		st=0
		sumt=0
		probafalsenegative=0
		for i in range(len(resproba)):
			
			a=utils.getPosition(target[i].player1,resproba[i])
			if dbtest!=None:
				prob=[]
				for k in range(4):
					plog=dbtest.getProbaPlayer(resproba[i][k][1],resproba[i][k][0])
					if plog!=0:		
						#prob.append(math.log10(plog))
						prob.append((plog))
					else:
						prob.append(-10000)
				str1=""
				
				if(a!=-1):
					plog=dbtest.getProbaPlayer(resproba[i][a][1],resproba[i][a][0])
					if plog!=0:		
						#prob.append(math.log10(plog))
						prob.append((plog))
					else:
						prob.append(-10000)
				else:
					prob.append(100)
			
			if (a==threshold or (threshold==200 and a>0)) and (prob[0]>treshProba or math.isnan(prob[0])):
				if(prob[0]< prob[1] or prob[0]<prob[2]):
						probafalsenegative+=1
						str1=("WARNING!!")
				stra=""

				for k in range(len(prob)):
					if(k==len(prob)-1):
						b=a
					else:
						b=k
					tab="\t"
					if(len(	resproba[i][b][0])<10):
						tab="\t\t"
					stra+=("{3}:{0}: {1} p:{2}|"+tab).format(resproba[i][b][0],round(resproba[i][b][1],2),round(prob[k],2),b)
				  
				print(("{0}:{1} |"+stra+str1).
				format(i,target[i].player1))
				st+=1
				sumt+=resproba[i][0][1]
				if(a>0):
					fail+=1
				if(a>2):
					bad_failure+=1
				if(resproba[i][0][1]>1):
					bad_replay+=1
		if (st!=0):			
			print("number of position {0}: {1} with mean value {2}| number of warning {3}".format(threshold,st,round(sumt/st,2),probafalsenegative))
		if(threshold==200):
			print("Number of games: {0},number of failure {1}({2})% , number of bad failure(>2) {3}({5}%) ,failure not bad {8}, bad replay {4}({6}%) bad failure less bad replay {7}({9}%)|{10} ".format(
			len(target),						
			fail,									
			round(float(fail)/len(target)*100,3),	
			bad_failure,
			bad_replay,
			round(float(bad_failure)/len(target)*100,2)
			,round(float(bad_replay)/len(target)*100,2)
			,bad_failure-bad_replay		#7
			,fail-bad_failure,
			round(float(s-bad_failure)/len(target),2),
			probafalsenegative))
			
			
			#################			

	def scoreProbaByPLayer(self,resproba,target):
		dtotal={}
		d0={}
		for i in range(len(target)):
			p=target[i].player1
			a=utils.getPosition(p,resproba[i])
			dtotal[p]=dtotal.get(p,0)+1
			if a==0:
				d0[p]=d0.get(p,0)+1
				
		for p in dtotal:
			print("{0} is at {3}% of success ({1} good,{4} bad, total: {2})".format(p,d0.get(p,0),dtotal[p],round(100*float(d0.get(p,0))/dtotal[p],2), dtotal[p]-d0.get(p,0)))
			
			
##################### TEST #######################
def main():
	print("run test")
	test()
#test path needs to have bad replay
#test path need to have bad p1 or p2 files	
def test():
	 #test rapide 
	testpath="../Replays/replaytest/2"
	testpath2="../Replays/replaytest/1"
	
	#test long
#	testpath="replayofficial/WCS15Season2"
#	testpath2="replayofficial/WCS15Season3"
	m=multipleDB()
	print ("test :addindg two dbs from ")
	m.addDb("test2",testpath)
	m.addDb("test3",testpath2)
	db1=m.DBs["test2"]
#	db1.calculateAC()
#	db1.calculateStatsAc()
#	print(db1.statsAC["maru"],db1.getProbaPlayer(0.86,"maru"))
#	print(db1.ac["maru"])
#	m.addDb("2",testpath2)
	print("test: updating matrix")
	#m.updateAllMatrixAlldb()
	print("test: updating APM")
	#m.updateAllAPMAlldb()
	print("test: evaluate DB")
	#m.DBs["2"].showPlayers()
	#res,tar=m.evaluateDB("1","2","basic")
	print("test:evaluate Proba")
	#res,target=m.evaluateDB("1","2","gap",coefMat=1,coefGap=1,coefApm=0,coefFreq=0)
	#print(m.scoreEval(res,target))
	res,target=m.evaluateProba("test2","test3","gap",fail=True,coefMat=1,coefGap=0,coefApm=0,coefFreq=0,coefMat3=0)
	m.scoreProba(res,target,200,m.DBs["test2"],-100000)
	print("END TEST")
	#print(m.scoreEval(res,tar))
if __name__ == '__main__':
    main()
    		
		

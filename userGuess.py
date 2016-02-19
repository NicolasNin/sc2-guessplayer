#sc2-guess
import os
import dbsc2
import multipledb

class userGuess(multipledb.multipleDB):
	def __init__(self):
		multipledb.multipleDB.__init__(self)
		self.dbreference=""
	def addSc2Replay(self,path,dbname):
		if dbname in self.DBs:
			(g1,g2)=self.DBs[dbname].addReplay(path)
		else:
			db=dbsc2.dbsc2(dbname)		
			(g1,g2)=db.addReplay(path)	
			self.DBs[dbname]=db
		return (g1,g2)
		
	def guessReplay(self,path,dbreference):
		(g1,g2)=self.addSc2Replay(path,"userReplay")
		if g1=="error" or g2=="error":
			return "error"
		#we have to test each player against dbreference
		#first we fit the data to the estimator (here we just give it the db)
		# but with different estimator
		#we do this only if self.dbreference is not equal to the one given
		
		if self.dbreference!= dbreference:
			self.dbreference=dbreference
			self.estimator.fit(self.DBs[dbreference],False)
		
		res1=self.estimator.giveProba(g1,method="manhattan",option=2,coefMat=1,coefGap=4,coefApm=1,coefFreq=1)
		res2=self.estimator.giveProba(g2,method="manhattan",option=2,coefMat=1,coefGap=4,coefApm=1,coefFreq=1)
		#now we got the result as res1 and res2

		self.displayResultGuess(res1,g1)
		self.displayResultGuess(res2,g2)
		return (res1,res2,g1,g2)
		
		
	def displayResultGuess(self,res1,g1):
		print("\nPlayer {0} in replay:".format(g1.name_in_replay1))
		
		for i in range(min(3,len(res1))):
			print("Guess number {0} as {1} with value {2} ".format(
			i+1,res1[i][2].player1,
			round(res1[i][1],2)))
		print("------------------------------------------")
	def guessDirectory(self,path,dbreference):
		for dirname, dirnames, filenames in os.walk(path):
			for filename in filenames:
				if filename[len(filename)-10:len(filename)]==".SC2Replay":
					print (os.path.join(dirname, filename))
					self.guessReplay(os.path.join(dirname, filename),dbreference)	
		
		
			
			
			
			
			
			
			
##################### TEST #######################
def main():
	print("run test")
	test()

def test():
	 #test rapide 
	testpath="replaytest/2"
	testpath3="replaytest/1"
	
	#test long
	#testpath="replayofficial/WCS15Season2"
	#testpath3="replayofficial/WCS15Season3"
	m=userGuess()
	print ("test :addindg two dbs from ")
	#m.addDb("1",testpath)
	m.addDb("2",testpath3)
#	(res1,res2,g1,g2)=m.guessReplay("replayperso/TVZ SNUTE.SC2Replay","3")
#	(res1,res2,g1,g2)=m.guessReplay("replayperso/noconvert/TVZSNUTE.SC2Replay","3")
	m.guessDirectory("replayperso/COHO","2")
	print("END TEST")
	#print(m.scoreEval(res,tar))
if __name__ == '__main__':
    main()

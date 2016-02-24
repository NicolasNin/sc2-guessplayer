#sc2-guess
import estimator
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
class corelation():
	def __init__(self):
		""" """
	def corelation(self,db1,liste1,db2,liste2,coefMat=1,coefGap=4,coefApm=0,coefFreq=0):
		E=estimator.PPVEstimator()
		if type(liste1)== str:
			liste1=[liste1]		
		if type(liste2)== str:
			liste2=[liste2]
		
		matrixcor=[]
		listegames1=[]
		listegames2=[]	
		missing_player=""
		#first we create the two games liste its quite redodnant with the matrix but easier
		for p1 in liste1:
			if(p1 in db1.players):
				for g1 in db1.players[p1]:
					listegames1.append(g1)
			else:
				missing_player+=" "+p1
		for p2 in liste2:
			if(p2 in db2.players):
				for g2 in db2.players[p2]:
					listegames2.append(g2)
			else:
				missing_player+=" "+p2 +" " + str(db1)
			
		if(missing_player!= ""):
			print("error player names not in one or two db", missing_player)
			return("missing player")
			
		for p1 in liste1:
			for g1 in db1.players[p1]:
				l=[]
				for p2 in liste2:
					for g2 in db2.players[p2]:
						l.append( E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=coefMat,coefGap=coefGap,coefApm=coefApm,coefFreq=coefFreq) )
					
				matrixcor.append(l)
		return (matrixcor,listegames1,listegames2)
	
	def autoCorelation(self,db,player,coefMat=1,coefGap=4,coefApm=0,coefFreq=0):
		return self.corelation(db,player,db,player,coefMat=coefMat,coefGap=coefGap,coefApm=coefApm,coefFreq=coefFreq)
	def test(self):
		print("test")
	def visualizeCorelation(self,db1,liste1,db2,liste2,coefMat=1,coefGap=4,coefApm=0,coefFreq=0,groupbyname=True):
		(mat,listeg1,listeg2)=self.corelation(db1,liste1,db2,liste2,coefMat=1,coefGap=0,coefApm=0,coefFreq=0)
		self.VisualizeMatrix(mat,listeg1,listeg2,True,groupbyname=groupbyname)
	def VisualizeMatrix(self,matrix,listegames1,listegames2,display=False,groupbyname=True,path="img/corelation"):			
		alpha=[];beta=[]
		prevname=""
		sizex=[]
		sizey=[]
		temp=0
		for g1 in listegames1:
			if groupbyname:
				if (g1.player1!=prevname):
					prevname=g1.player1
					alpha.append(g1.player1)
					sizey.append(temp)
					temp+=1
				else:
					temp+=1
			else:
				alpha.append(g1.player1)
		prevname=""
		temp=0
		for g2 in listegames2:
			if groupbyname:
				if (g2.player1!=prevname):
					prevname=g2.player1
					beta.append(g2.player1[0:min(len(g2.player1),1)])
					sizex.append(temp)
					temp+=1
				else:
					temp+=1
			else:
				beta.append(g2.race2)
	#	n=0	
	#	for p in listegames1:
	#		print("{0] vs {1}".format(n,p.player1,p.player2))
	#		n+=1
		
		fig = plt.figure()
		ax = fig.add_subplot(111)
		cax = ax.matshow(matrix)
		if groupbyname:
			print(sizey,alpha)	
			print(sizex,beta)	
			ax.set_yticks(sizey)
			ax.set_yticklabels(alpha)	
			ax.set_xticks(sizex)
			ax.set_xticklabels(beta)	
		else:
			ax.set_xticklabels([''] +beta)
			ax.set_yticklabels([''] +alpha)
			ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
			ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

		
		fig.colorbar(cax)
		if display==True:
			plt.show()
		print("before save",os.getcwd())
		name="corelation"+str(time.clock())+".png"
		fig.savefig(path+name)
		return name		


"""
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(l)
ax.set_yticks(size)
ax.set_yticklabels(alpha)
plt.show()
"""
##########TEST###############
def main():
	print("run test")
	import userGuess
	m=m=userGuess.userGuess()
	m.addDb("3","../replayofficial/WCS15Season3")
	m.addDb("hs12","../replayofficial/HS12")
	db3=m.DBs["3"]
	dbhs=m.DBs["hs12"]
			
	c=corelation()
	(m,l1,l2)=c.corelation(db3,"snute",db3,"snute",coefGap=0)
	print(c.VisualizeMatrix(m,l1,l2))
if __name__ == '__main__':
	main()

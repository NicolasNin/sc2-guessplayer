#sc2-guess
import estimator
import utils
import multipledb
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import numpy as np
#import graphviz as gv
#####
def getL(db,player):
	L=[]
	for g in db.players[player]:
		L.append(g.frequency_of_gap)
	return L
def visufrequency(db,player):
	L=[]
	for i in db.players[player]:
		L.append(i.frequency_of_hotkeys)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	cax = ax.matshow(L,aspect="auto")
	fig.colorbar(cax)
	plt.show()	
def visugap(l):
	L=[]
	for i in l:
		ab=[]
		for j in range(15):
			ab.append(i.get(j,0))
		L.append(ab)	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	cax = ax.matshow(L,aspect="auto")
	fig.colorbar(cax)
	plt.show()	
#####visu hotkey 
def visuHotkey(db,player,n):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	
	x=[]
	y=[]
	z=[]
	i=0
	for j in range(0,min(10,len(db.players[player]))):
		for f in range(len(db.players[player][j].frame)):
			if f<10000:
				x.append(db.players[player][j].frame[f])
				z.append(db.players[player][j].hotkeys[f])
				y.append(i)
			else:
				break
		i+=1
	"""	
	for i in range(len(db.players[player][0].frame)):
		x.append(db.players[player][0].frame[i])
		y.append(db.players[player][0].hotkeys[i])
		z.append(0)
	for i in range(len(db.players[player][1].frame)):
		x.append(db.players[player][1].frame[i])
		y.append(db.players[player][1].hotkeys[i])
		z.append(1)
	"""
	
	ax.scatter(x, y, z,  marker='o')

	#plt.scatter(x, y,z)
	plt.show()
############################
from numpy import mean,std
import math
def cumulativeDistribNormal(m,s,a):
	return 0.5*( 1+math.erf( (a-m)/(s*math.sqrt(2))) )

def getProba(db,score,player):
	acmean=getMeanAuto(db)
	m=acmean[player][0]
	s=acmean[player][1]
	return 1-cumulativeDistribNormal(m,s,score)
	
def getMeanAuto(db):
	ac=autocorelation(db)
	l=[]
	res={}
	for p in ac:
		l=[]
		for i in ac[p][0]:
				
			for j in i:
				if (j!=0):
					
					l.append(j)
		if(len(l)==0):
			print("not enough not nul number or equivalently only one replay")
			#return (0,0)
			res[p]=(0,0)
		res[p]=(mean(l),std(l),len(l),len(ac[p][0]))
	return res
def autocorelation(db,MU=False,coefMat=1,coefGap=4,coefApm=0,coefFreq=0):
	ac={}
	for i in db.players:
	#	print(i,len(db.players))
		ac[i]=correlation(db,i,db,i,MU,coefMat,coefGap,coefApm,coefFreq)
	return ac

def correlation(db1,p1,db2,p2,MU=False,coefMat=1,coefGap=4,coefApm=0,coefFreq=0):
	
	cor=[]
	E=estimator.PPVEstimator()
	G1=[]
	G2=[]
	if MU:
		for r in ["T","P","Z"]:
			for g1 in db1.players[p1]:
					if g1.race2==r:
						G1.append(g1)
			for g2 in db2.players[p2]:
					if g2.race2==r:
						G2.append(g2)
		for g1 in G1:
			l=[]
			for g2 in G2:
				l.append(E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=coefMat,coefGap=coefGap,coefApm=coefApm,coefFreq=coefFreq))
			cor.append(l)
		return (cor,G1,G2)
	else:
		for g1 in db1.players[p1]:
			l=[]
			for g2 in db2.players[p2]:
				l.append(E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=coefMat,coefGap=coefGap,coefApm=coefApm,coefFreq=coefFreq))
			cor.append(l)
		return (cor,db1.players[p1],db2.players[p2])

def visualizeMatrix2(m,size,labl):#with irregular ticks
		fig = plt.figure()
		ax = fig.add_subplot(111)
		cax = ax.matshow(m)
		ax.set_yticks(size)
		ax.set_yticklabels(labl)
		fig.colorbar(cax)
		plt.show()
#		ax.xticks(tick_locs, tick_lbls)
#		ax.yticks(tick_locs, tick_lbls)
		#ax.set_xticklabels(size,labl)
		#ax.set_yticklabels(size,labl)
		
#		ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
#		ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

		
"""		

"""		
def visualizeMatrix(m,source=None):
	
	if source ==None:
		fig = plt.figure()
		ax = fig.add_subplot(111)
		cax = ax.matshow(m,aspect='auto')
		fig.colorbar(cax)
		
		plt.show()
	else:
		alpha=[]
		beta=[]
		for g1 in source:
			#alpha.append(g1.name_in_replay1[0]+""+g1.path[15:-12])
			alpha.append(g1.player1)
			
		for g2 in source:
			beta.append(g2.race2)
		n=0	
		for p in source:
			print("{0}:Replay Name: {1}|path : {2}".format(n,p.name_in_replay1,p.path[14:-12]))
			n+=1
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_xticklabels([''] +beta)
		ax.set_yticklabels([''] +alpha)
		cax = ax.matshow(m,aspect='auto')
		fig.colorbar(cax)
	#	ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
	#	ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
		plt.show()		

def visualizeAC2(db,player,MU=False,coefMat=1,coefGap=4,coefApm=0,coefFreq=0):
	visualizeAC(db,player,db,player,MU,coefMat,coefGap,coefApm,coefFreq)
def visualizeAC(db,player,db2,player2,MU=False,coefMat=1,coefGap=4,coefApm=0,coefFreq=0):
	(ac,G1,G2)=correlation(db,player,db2,player2,MU,coefMat,coefGap,coefApm,coefFreq)
	#print(len(ac),len(G1),len(G2))
	#ac=ac[len(ac)-40:len(ac)-20]
	#G1=G1[len(G1)-40:len(G1)-20]
	#G2=G2[len(G2)-40:len(G2)-20]
	#print(len(ac),len(G1),len(G2))
#	alpha = ['ABC', 'DEF', 'GHI', 'JKL']
	alpha=[]
	beta=[]
	
	for g1 in G1:
		alpha.append(g1.player2+"("+g1.race2+")")
	for g2 in G2:
		beta.append(g2.race2)
	print (alpha)
	print(beta)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_xticklabels([''] +beta)
	ax.set_yticklabels([''] +alpha)
	cax = ax.matshow(ac,aspect='auto')
	fig.colorbar(cax)
	ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
	ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
	plt.show()	

#-------------------------
def distanceSetofGames(set1,set2):
	E=estimator.PPVEstimator()
	d=[]
	for g1 in set1:
		l=[]
		for g2 in set2:
			l.append(E.score(g1,g2,method="gap"))
		#d.append(float(sum(l))/len(l))
		d.append(utils.minnotnul(l))
	return sum(d)/len(d)

def distancePlayers(db1,player1,db2,player2):
	return distanceSetofGames(db1.players[player1],db2.players[player2])

def distancePlayerSamedb(db1,player1,player2):
	return distanceSetofGames(db1.players[player1],db1.players[player2])
def matrixDistancePlayer2(db1,db2):
	cor=[]
	listeplayer=[]
	for p1 in db1.players:
		race1=db1.players[p1][0].race1
		l=[]
		listeplayer.append(p1)
		for p2 in db2.players:
			if(race1==db2.players[p2][0].race1):
				l.append(distancePlayers(db1,p1,db2,p2))
			else:
				l.append(distancePlayers(db1,p1,db2,p2))
		cor.append(l)
	print(listeplayer)	
#	for i in range(len(cor)):
#		print(listeplayer[i],cor[i])
	return (cor,listeplayer)

def matrixDistancePlayer(db1):
	cor=[]
	listeplayer=[]
	for p1 in db1.players:
		race1=db1.players[p1][0].race1
		l=[]
		listeplayer.append(p1)
		for p2 in db1.players:
			if(race1==db1.players[p2][0].race1):
				l.append(distancePlayerSamedb(db1,p1,p2))
			else:
				l.append(distancePlayerSamedb(db1,p1,p2))
		cor.append(l)
	print(listeplayer)	
#	for i in range(len(cor)):
#		print(listeplayer[i],cor[i])
	return (cor,listeplayer)

def createGraphfromMatrix(mat,label,t=1.1):
	g1 = gv.Graph(format='svg')
	for i in range(len(mat)):
		g1.node(label[i])
		for j in range(i+1,len(mat[0])):
			print(i,j)
			if(mat[i][j]<t):
				g1.edge(label[i],label[j],weight=str(mat[i][j]))
	return g1			
def main():
	print("run test")
	testcorel()
def testcorel():
	m=multipledb.multipleDB()
	testpath1="replaytest/1"
	testpath2="replaytest/2"
	m.addDb("2",testpath2)
	m.addDb("1",testpath1)
	ac=autocorelation(m.DBs["1"])
	#print(ac["maru"])
	visualizeAC(m.DBs["1"],"maru")
def test():
	 #test rapide 
	testpath="replaytest/2"
	testpath2="replaytest/1"
	
	#test long
	testpath2="replayofficial/WCS15Season2"
	#testpath2="replayofficial/HS12"
	#testpath3="replayofficial/NW3"
	
	m=multipledb.multipleDB()
	print ("test :addindg two dbs from ")
	#m.addDb("1",testpath)
	m.addDb("2",testpath2)
#	m.addDb("3",testpath3)
	#print("aa",distancePlayerSamedb(m.DBs["2"],"maru","maru"))
	#print("aa",distancePlayerSamedb(m.DBs["2"],"soo","soo"))
	(mat,player)=matrixDistancePlayer(m.DBs["2"])
	#g2=createGraphfromMatrix(mat,player)
	#g2.render('test')
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	cax = ax.matshow(mat)
	fig.colorbar(cax)
	plt.show()
	
	
	"""
	print(distancePlayers(m.DBs["1"],"maru",m.DBs["1"],"soo"))
	print(distanceSetofGames(m.DBs["1"].players["soo"],
	m.DBs["1"].players["maru"]))
	print(distanceSetofGames(m.DBs["1"].players["soo"],
	m.DBs["1"].players["maru"]))
	"""
	print("END TEST")
	#print(m.scoreEval(res,tar))
if __name__ == '__main__':
	main()

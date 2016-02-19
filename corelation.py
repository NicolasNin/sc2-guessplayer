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
def autocorelation(db):
	ac={}
	for i in db.players:
		print(i,len(db.players))
		ac[i]=correlation(db,i,db,i)
	return ac

def correlation(db1,p1,db2,p2):
	cor=[]
	E=estimator.PPVEstimator()
	G1=[]
	G2=[]
	if 1==0:
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
				l.append(E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=0,coefGap=4,coefApm=0,coefFreq=0))
			cor.append(l)
		return (cor,G1,G2)
	else:
		for g1 in db1.players[p1]:
			l=[]
			for g2 in db2.players[p2]:
				l.append(E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=1,coefGap=0,coefApm=0,coefFreq=0))
			cor.append(l)
		return (cor,db1.players[p1],db2.players[p2])

def visualizeAC2(db,player):
	visualizeAC(db,player,db,player)
def visualizeAC(db,player,db2,player2):
	(ac,G1,G2)=correlation(db,player,db2,player2)
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

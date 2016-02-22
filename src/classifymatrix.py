#sc2-guess

#we are given a symetrical matrix of "distance"  (nXn)can be seen as araph  
#we are looking for a way to separate the n entry into groups such that 
#the max of the distance in this group is at most alpha
#ofcourse if alpha is too small we have to put each entry into its own 
#class, and if alpha is too big there is no need to cut

#a good cut is one that drastically reduce distance within the groups
#ie if we decide to not have two entries in the same group closer than
# alpha, then its better to not have too much entries closer to alpha
#in the subgroup created

#this can easily be twice faster but im lazy today
#note that the time i took to write this is longer that the time it would take to make the change needed

#one problem is that there is mutliple solution
#indeed is 1 close to 2 close to 3 and 1 not close to 3 we have to cut two of the close one

#it is the graphe connectivity problem!!!!
def createSubgroup(matrix,alpha):
	equivalence=[]
	for i,row in enumerate(matrix):
		for j,value in enumerate(row):
			
			if value<alpha and i!=j :
				equivalence.append((i,j))
				
	return disjoint_sets(equivalence)
	
def createAllGroupe(ac,alpha):
	g={}
	for p in ac:
		g[p]=createSubgroup(ac[p][0],alpha)
	return g

def reorganizeMatrix2(matrix,liste_player,db):
		E=estimator.PPVEstimator()
		nouvellematrice=[]
		l=[]
		for i1 in liste_player:
			for g1 in db.players[i1]:
				l=[]
				for i2 in liste_player:
					for g2 in db.players[i2]:
							#print(i1,i2,g1,g2)
							l.append(E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=1,coefGap=4,coefApm=0,coefFreq=0))
				nouvellematrice.append(l)
		return nouvellematrice

def reorganizeMatrix(matrix,source,group):
	newm=[]
	news=[]
	for s in source:
		news.append(s)
	for g1 in group:
		for i in g1:
			l=[]
			for g2 in group:
				for j in g2:
					l.append(matrix[i][j])
			newm.append(l)
	return (newm,news)
"""	"	
for p in allgroup:
	if len(allgroup[p])>1:
		print(p,len(allgroup[p]))
		#corelation.visualizeAC(m.DBs["allwcs"],p,m.DBs["allwcs"],p,False,coefMat=1,coefGap=0,coefApm=0,coefFreq=0)
		newm=reorganizeMatrix(ac[p][0],allgroup[p])
		corelation.visualizeMatrix(newm)
		for i in allgroup[p]:
			print(len(i))
"""
def findAlpha(ac,p,maxgroup=2):
	mini=0.
	maxi=2.
	m=1
	for i in range(10):
		m=(mini+maxi)/2
		group=createSubgroup(ac[p][0],m)
		
		if (len(group)>=maxgroup):
			mini=m
		else:
			maxi=m
	return mini


def reverseLvl(matrix,lvlmin):
	grouperef=createSubgroup(matrix,lvlmin)
	maxgroup=len(grouperef)
	mini=0
	maxi=5
	for i in range(11):
		m=(mini+maxi)/2
		group=createSubgroup(matrix,m)
		if (len(group)>=maxgroup):
			mini=m
		else:
			maxi=m
	return mini
	
def findMean(indices,matrix):
	maxi=0
	sum0=0
	n=0
	for i in indices:
		l=[]
		for j in indices:
			if j!=i:
				sum0+=matrix[i][j]
				n+=1

	return sum0/n
def getSubMatrix(matrix,deb,end):
	d=[]
	for i in range(deb,end):
		l=[]
		for j in range(deb,end):
			l.append(matrix[i][j])
		d.append(l)
	return d
def MultiComportment(ac,t,op=True,maxgroup=2):
	l=[]
	for p in ac:
		lvl=findAlpha(ac,p,maxgroup)
		g=createSubgroup(ac[p][0],lvl)
		
		if not op:
			if lvl>t:
				l.append((p,lvl,g))
				print(p,lvl,len(g))
		else:
			if lvl<t:
				l.append((p,lvl))
				print(p,lvl)
	for (p,alpha,g)in l:
		print(p,alpha,"minmax",findMean(range(len(ac[p][0])),ac[p][0]))
		for sg in g:
			print (len(sg))
		(newm,news)=reorganizeMatrix(ac[p][0],ac[p][1],g)
		deb=0
		"""
		for sg in g:
			end=len(sg)+deb
			print(p,deb,end,"minmax local",findMean(sg,ac[p][0]))
		"""	
		corelation.visualizeMatrix(newm,news)
			#deb=len(sg)
	return l
#http://stackoverflow.com/questions/20154368/union-find-implementation-using-python
def indices_dict(lis):
	d = {}
	for i,(a,b) in enumerate(lis):
		if a not in d:
			d[a]=[]
		temp=d[a]
		temp.append(i)
		d[a]=temp
		if b not in d:
			d[b]=[]
		temp=d[b]
		temp.append(i)
		d[b]=temp
	return d

def disjoint_indices(lis):
	d = indices_dict(lis)
	sets = []
	while len(d):
		que = set(d.popitem()[1])
		ind = set()
		while len(que):
			ind |= que 
			que = set([y for i in que 
				for x in lis[i] 
				for y in d.pop(x, [])]) - ind
		sets += [ind]
	return sets

def disjoint_sets(lis):
	return [set([x for i in s for x in lis[i]]) for s in disjoint_indices(lis)]
    
    
def BigMatrix(db,liste_player,coefMat=1,coefGap=4):
	E=estimator.PPVEstimator()
	s=[]
	bigm=[]
	size=[]
	name=[]
	sizetemp=0
	total_size=len(liste_player)
	i=0
	for p1 in liste_player:
		i+=1
		print(i, total_size)
		size.append(sizetemp)
		sizetemp+=len(db.players[p1])
		name.append(p1)
		for g1 in db.players[p1]:
			l=[]
			s.append(g1)
			
			for p2 in liste_player:
				for g2 in db.players[p2]:
					l.append(E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=coefMat,coefGap=coefGap,coefApm=0,coefFreq=0))
					#l.append( corelation.correlation(db,p1,db,p2,MU=False,coefMat=1,coefGap=4,coefApm=0,coefFreq=0)[0]    )
			bigm.append(l)
	return (bigm,s,size,name)		

def NameInGroup(group,liste_player):
	lp=[]
	for p in liste_player:
		for g in liste_player[p]:	
			lp.append(p)
	groupname=[]
	groupsize=[]		
	temp=0
	for g in group:
		groupsize.append(temp)
		temp+=len(g)
		l=[]
		gname=""
		for i in g:			
			if lp[i] not in l:
				l.append(lp[i])
				gname+=lp[i][0:min(lp[i],5)]+" "
		print (l,len(g))
		groupname.append(gname)
	return (groupname,groupsize)
	
for i in range(len(namehero)):
	if temp%3==0:
		namehero[i]=(namehero[i].rstrip())[0:min(len(namehero[i]),5)]
	elif temp%3==1:
		namehero[i]=(namehero[i].rstrip())[0:min(len(namehero[i]),5)]+"                           "
	else:
		namehero[i]=(namehero[i].rstrip())[0:min(len(namehero[i]),5)]+"                                                        "	
	temp+=1		
	
	

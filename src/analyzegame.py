#sc2-guessplayer
import game
import utils
class AnalyzeGame():
	""" class of methods to get stats for a game"""
	def __init__(self,game):
		self.game=game
	
	def frequency_of_frame_gap(self,frame):
		freq={}
		size=len(frame)
		if size<2:
			print("not enough frame")
			return freq
		prev=frame[0]
		for i in range(1,size):
			a=frame[i]-prev
			freq[a]=freq.get(a,0)+1
			prev=frame[i]
		return freq

def frequency_of_frame_gap(frame):
	freq={}
	
	size=len(frame)
	if size<2:
		print("not enough frame")
		return freq
	prev=frame[0]
	for i in range(1,size):
		a=frame[i]-prev
		freq[a]=freq.get(a,0)+1
		prev=frame[i]
	return freq

def PlayerGapFrequency(db,player):	
	l=[]
	for g in db.players[player]:
		
		l.append(normalize(frequency_of_frame_gap(g.frame)))
	return l

def normalize(d):
	 s=sum(d.values())
	 for i in d:
		 d[i]=float(d[i])/s
	 return d

def statGapPLayer(db,player):
	l=PlayerGapFrequency(db,player)
	statGapPLayer2(l)

def statGapPLayer2(l):
	meanz=[]
	for i in range(10):
		s=0
		size=len(l)
		print("looking at gap of size",i)
		for d in l:
			s+=d[i]
			print(round(d[i]*100,1))
		meanz.append(round(s/size*100))
	print( meanz)
	

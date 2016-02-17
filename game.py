#sc2-guessplayer
import alias
import utils

class game():
	def __init__(self,j1,j2,race1,race2,hotkeys,frame,path="",mapsc2="",length="",date=""):
		#we change the name of player with known aliases
		#we arbitrary
		self.name_in_replay1=j1
		self.name_in_replay2=j2
		self.player1=alias.get(j1)
		self.player2=alias.get(j2)
		
		#we only keep the first letter 
		if len(race1)>0:
			self.race1=race1[0]
		if len(race2)>0:
			self.race2=race2[0]	
		#important data we need frame to be not empty
		self.hotkeys=hotkeys	
		self.frame=frame
		self.last_frame=frame[len(frame)-1]
		#stuff to be calculated THOSE ARE THE FEATURE DEPENDING ON ESTIMATOR
		self.matrix=[]
		self.APM=-1
		self.frequency_of_hotkeys=[0,0,0,0,0,0,0,0,0,0]
		self.frequency_of_gap={}
		
		#to be sure that data calculated are consitent
		self.APM_calculated_with_limits=-1
		self.matrix_calculated_with_limits=-1
		#other info from replay not that important at first
		self.path=path	#path in system to find replay if necessary
		self.mapsc2=mapsc2
		self.date=date
		self.length=length
	def calculateFrequencyGap(self):
		freq={}
		size=len(self.frame)
		if size<2:
			print("not enough frame")
			return freq
		prev=self.frame[0]
		for i in range(1,size):
			a=self.frame[i]-prev
			freq[a]=freq.get(a,0)+1
			prev=self.frame[i]
		self.frequency_of_gap=freq
		utils.normalize_dict(self.frequency_of_gap)
		 
	def calculate_frequency(self,limit=10000,limitelow=0):
		last=min(limit,self.last_frame)
		for i in range(len(self.hotkeys)):
			touche=self.hotkeys[i]
			if self.frame[i]> limitelow:
				if self.frame[i]>last:
					break
				self.frequency_of_hotkeys[touche]+=1
		s=sum(self.frequency_of_hotkeys)
		for i in range(len(self.frequency_of_hotkeys)):
			self.frequency_of_hotkeys[i]=float(self.frequency_of_hotkeys[i])/s
				
	def calculate_matrix(self,limit=10000,limitelow=0):
		self.matrix_calculated_with_limits=limit
		#initalize 10X10 matrix kinda dirty
		self.matrix=[[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10]
		prev=-1
		last=min(limit,self.last_frame)
		for i in range(len(self.hotkeys)):
			touche=self.hotkeys[i]
			if self.frame[i]> limitelow:
				if self.frame[i]>last:
					break
				if prev!=-1:
					self.matrix[prev][touche]+=1
				prev=touche
	def normalize_matrix(self):
		utils.normalize_matrix(self.matrix)
	def calculateAPMj1(self,limit=10000):
		self.APM_calculated_with_limites=limit
		prev=0
		liste_ecart=[]
		for i in self.frame:
			if i>limit:
				break
			else:
				if(i-prev<50):
					liste_ecart.append(i-prev)
				prev=i
		self.APM=(float(sum(liste_ecart))/len(liste_ecart))
		return self.APM		

import sys
import sc2reader
import glob, os
from dbsc2 import *

f = open('workfile', 'w')

def writeArrayToFile(arr1,arr2,filename,str1=None):
	if len(arr1)!=len(arr2):
		print("different size")
	else:	
		f=open(filename,'w')
		if str1!=None:
			f.write(str1+"\n")
		for i in range(len(arr1)):
			f.write(str(arr1[i]))
			f.write("\t")
			f.write(str(arr2[i]))
			f.write("\n")
		f.close()

class ConvertSc2Replay(DataBase_SC2):
	def __init__(self):
		""" """
		self.players={}
		
	def convertReplayFromPath(self,path):
		self.convertReplay(sc2reader.load_replay(path),path),
	def convertReplay(self,replay,filename):
	
		self.addReplay(replay)	
		#the replay is now added as a games in db
		#with the name of the two playesr
		names=[]
		races=[]
		for i in replay.players:
			names.append(i.name)
			races.append(i.pick_race)
		
		n1=len(self.players[names[0]])-1
		n2=len(self.players[names[1]])-1
		#the games of the two players
		g1=self.players[names[0]][n1]
		g2=self.players[names[1]][n2]
		
		#the file for player1
		str1=names[0]+"\n"+names[1]+ "\n" + races[0][0]+"\n"+races[1][0]
		str2=names[1]+" \n"+names[0]+ "\n" + races[1][0]+'\n'+races[0][0]
		
		print("writing "+filename)
		writeArrayToFile(g1.hotkeys,g1.frame,filename+"p1",str1)
		writeArrayToFile(g2.hotkeys,g2.frame,filename+"p2",str2)
	def convertAllDir(self,path):
		""" will convert all sc2files in path recursively"""
		som=0
		for dirname, dirnames, filenames in os.walk(path):
			for filename in filenames:
				som+=1
		som2=1
		for dirname, dirnames, filenames in os.walk(path):
			for filename in filenames:
				if filename[len(filename)-10:len(filename)]==".SC2Replay":
					if ( os.path.exists(os.path.join(dirname, filename)+"p1") and os.path.exists(os.path.join(dirname, filename)+"p1")):
						print("already done")
					else:
						print("writing",filename,som2,"/",som)
						self.convertReplayFromPath(os.path.join(dirname, filename))
					som2+=1				
		
		


def main():
	path = sys.argv[1]
	db=ConvertSc2Replay()
	db.convertAllDir(path)	
if __name__ == '__main__':
    main()

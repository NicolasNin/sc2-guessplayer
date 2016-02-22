#sc2-guess

#some fun with visu

import numpy as np
import cv2
import math 
import multipledb

m=multipledb.multipleDB()
m.addDb("hs12","replayofficial/HS12")

img = np.zeros((1000,1000,3), np.uint8)
cv2.circle(img,(500,500), 200, (255,255,255), -1)
cv2.circle(img,(500,500), 250, (0,255,255), -1)

x=[]
y=[]
n=10
for i in range(n):
	x.append(200*math.cos(2*math.pi*i/n)+500) 
	y.append(200*math.sin(2*math.pi*i/n)+500)
	

def numbers(x,y):
	for i in range(n):
		print("xyxyxy")
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(img,str(i),(int(x[i]),int(y[i])), font, 0.5,(153,153,0),2,cv2.CV_AA)

def linecircle(i,j,size,color,maxi,val):
#	print(i,j,size,maxi,val)
	if size!=0:
		print(i,j,size,maxi,val,int(val/maxi*10))
		cv2.line(img,(int(x[i]),int(y[i])),(int(x[j]),int(y[j])),(100,100,color),int(val/maxi*10))
#def mactrixcircle(matrix):

def maxmat(matrix):
	maxi=0
	for i in matrix:
		for j in i:
			if(j>maxi):
				maxi=j
	return maxi
def drawmatrix(matrix):
	
	maxi=maxmat(matrix)
			
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			linecircle(i,j,int(matrix[i][j]*255),int(matrix[i][j]/maxi*255),maxi,matrix[i][j])


def showcircleplayer(player,n=0):
	print(m.DBs["hs12"].players[player][n].matrix)
	drawmatrix(m.DBs["hs12"].players[player][n].matrix)
	numbers(x,y)
	cv2.imshow(player+" "+m.DBs["hs12"].players["dayshi"][n].player2
	
	
	
	
	 +str(n),img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()	

for p  in m.DBs["hs12"].players:
	print(p)
	img = np.zeros((1000,1000,3), np.uint8)

	cv2.circle(img,(500,500), 1000, (255,255,255), -1)
	cv2.circle(img,(500,500), 200, (0,0,0), -1)
	cv2.circle(img,(500,500), 199, (255,255,255), -1)

#	for i in range(len(m.DBs["hs12"].players[p])):
	for i in range(10):
		showcircleplayer("dayshi",i)
	

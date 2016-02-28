#sc2-guessplayer
import math
def minnotnul(l):
	mini=-1
	for i in l:
		if i!=0 and(mini>i or mini==-1):
			mini=i
	return mini
def normalize_matrix(matrix):
	somme=0
	for i in matrix:
		for j in i:
			somme+=j
	if somme!=0:
		for i in range(len(matrix)):
			for j in range(len(matrix[0])):
				matrix[i][j]=float(matrix[i][j])/somme
	else:
		print(self.player_name,self.adversary,"empty")

def normalize_dict(d):
	 s=sum(d.values())
	 for i in d:
		 d[i]=float(d[i])/s
	 return d
		
		
def distancedict(d1,d2,maxvalue):
	som=0
	for i in range(maxvalue):
		som+=abs(d1.get(i,0)-d2.get(i,0))
	return som	

def distancearray(arr1,arr2,maxbreak=100):
	som=0
	for i in range(len(arr1)):
		som+=abs(arr1[i]-arr2[i])
		if som>=maxbreak:
			return som
	return som		
def manhattan(matrix1,matrix2,maxbreak=10,puissance=1):
	#both matrix must have the same dimension
	som=0
	for line in range(10):
		for col in range(10):
			if som>=maxbreak:
				return som
			som+=math.pow(abs(matrix1[line][col]-matrix2[line][col]),puissance)
	return math.pow(som,1/puissance)

def getPosition(name,liste):
	for i in range(len(liste)):
		if (name==liste[i][0]):
			return i
	return -1	
##################### TEST #######################
def main():
	print("run test")
	test()

def test():
	print(test)
if __name__ == '__main__':
    main()
    

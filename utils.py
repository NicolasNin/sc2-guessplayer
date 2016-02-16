#sc2-guessplayer

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
		
def manhattan(matrix1,matrix2):
	#both matrix must have the same dimension
	som=0
	for line in range(10):
		for col in range(10):
				som+=abs(matrix1[line][col]-matrix2[line][col])
	return som

def getPosition(name,liste):
	for i in range(len(liste)):
		if (name==liste[i][0]):
			return i	
##################### TEST #######################
def main():
	print("run test")
	test()

def test():
	print(test)
if __name__ == '__main__':
    main()
    

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

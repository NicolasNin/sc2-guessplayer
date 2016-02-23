import pickle
import sys,os


def main():
	if len(sys.argv)==1:
		print("a path to a replay or a directory is required")
		return 0
	path = sys.argv[1]
	if path=="":
		print("a path to a replay or a directory is required")
	else:
		m=pickle.load(open("../save/dbserver","rb"))
		if(os.path.isdir(path)):
			m.guessDirectory(path,"all",coefMat=1,coefGap=4)
		else:	
			m.guessReplay(path,"all",coefMat=1,coefGap=4)

if __name__ == '__main__':
    main()

import pickle
import userGuess

def main():
	
	m=userGuess.userGuess()
	"""
	m.addDb("1","replayofficial/WCS15Season1")
	
	m.addDb("2","../replayofficial/WCS15Season2")
	m.addDb("3","../replayofficial/WCS15Season3")
	m.addDb("hs","replayofficial/HS12")
	m.addDb("nw3","replayofficial/NW3")
	m.addDb("ndh","replayofficial/dh")
	m.addDb("iem","replayofficial/iem")
	"""
	#TODODODOODODODODOODO: ajouter une db a une autre
	m.addDb("all","replayofficial/NOPE")
#	m.DBs["all"].addDirectory("../replayofficial/WCS14Season2")
#	m.DBs["all"].addDirectory("../replayofficial/WCS14GBSeason 3")
	m.DBs["all"].addDirectory("../replayofficial/WCS15Season1")
	m.DBs["all"].addDirectory("../replayofficial/WCS15Season2")
	m.DBs["all"].addDirectory("../replayofficial/WCS15Season3")
	m.DBs["all"].addDirectory("../replayofficial/HS12")
	m.DBs["all"].addDirectory("../replayofficial/NW3")
	m.DBs["all"].addDirectory("../replayofficial/dh")
	#	m.DBs["all"].addDirectory("replayperso")
	
	pickle.dump(m,open("../save/dbserver","wb"))
	

if __name__ == '__main__':
    main()

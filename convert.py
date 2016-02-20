#sc2-guess
import sc2reader
import game


def convertReplay(path,limit=15000):
	replay=sc2reader.load_replay(path)
	players=[]
	races=[]
	for i in replay.players:
		players.append(i.name)
		races.append(i.pick_race)
	if(len(players)>2):
		print("error: replay not 1v1 "+path)
		return ("error","error")
	hot={}
	frame={}
	hot[players[0]]=[]
	hot[players[1]]=[]
	frame[players[0]]=[]
	frame[players[1]]=[]
	for event in replay.events:
		if event.frame>=limit:
			break
		if event.name=="GetControlGroupEvent" or event.name=="SetControlGroupEvent" or event.name=="AddToControlGroupEvent" :
			hot[event.player.name].append(event.hotkey)
			frame[event.player.name].append(event.frame)
	
#mapsc2="",length="",date=""
	if (len(hot[players[0]])>10):				
		g1=game.game(players[0],players[1],races[0],races[1],hot[players[0]],frame[players[0]],path,replay.map_name,replay.length,replay.date)
	else:
		g1="error"
		print("error, not enough frame")
	if (len(hot[players[1]])>10):
		g2=game.game(players[1],players[0],races[1],races[0],hot[players[1]],frame[players[1]],path)
	else:
		g2="error"
		print("error, not enough frame")		
	return (g1,g2)
	
##################### TEST #######################
def main():
	print("run test")
	test()

def test():
	convert("replayperso/TVZ SNUTE.SC2Replay")

	print("END TEST")
if __name__ == '__main__':
    main()	

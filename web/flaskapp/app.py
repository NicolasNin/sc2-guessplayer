import sys,os
from flask import Flask, render_template, request,redirect, url_for,jsonify
from werkzeug import secure_filename
import pickle
path_abs=os.path.abspath(".")+"/"


if path_abs=="/home/sc2guess/":
		path_abs="/home/sc2guess/sc2-guessplayer/web/flaskapp/"
sys.path.insert(0, path_abs+'/../../src')
import corelation
import estimator


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = path_abs+"replayuploaded"
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
ALLOWED_EXTENSIONS = set(["sc2replay"])

m=pickle.load(open(path_abs+"../../save/dbserver","rb"))



dict_of_result={}
def allowed_file(filename):
    return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
EVENT=["Unknwown","WCS15S1","WCS15S2","WCS15S3","NW3","HS12","DH"]
EventUrl=["","http://wiki.teamliquid.net/starcraft2/2015_WCS_Season_1/",
"http://wiki.teamliquid.net/starcraft2/2015_WCS_Season_2",
"http://wiki.teamliquid.net/starcraft2/2015_WCS_Season_3",
"http://wiki.teamliquid.net/starcraft2/NationWars_III",
"http://wiki.teamliquid.net/starcraft2/HomeStory_Cup/12",
"http://wiki.teamliquid.net/starcraft2/2016_DreamHack_Open/Leipzig"]
liste_player=[]
for i in m.DBs["all"].players:
	liste_player.append(i)
def event(path):
	if path[18:30]=="WCS15Season1":
		return 1
	if path[18:30]=="WCS15Season2":
		return 2
	if path[18:30]=="WCS15Season3":
		return 3
	if path[18:21]=="NW3":
		return 4
	if path[18:22]=="HS12":
		return 5
	if path[18:20]=="dh":
		return 6
	else:
		return 0

@app.route('/comparegroupsgraphe')
def comparegroup2():
	return render_template("graphemany.html",liste=liste_player)

@app.route('/comparegroups')
def comparegroup():
	return render_template("matrixmany.html",liste=liste_player)
@app.route('/matrix2/<player>/<t>')
def matrix(player,t):
	player=getDBname(player)
	return render_template("matrix_visu.html",player=player,t=t)
	
@app.route('/graphe/<player>/<t>')
def graphe(player,t):
	player=getDBname(player)
	
	return render_template("temgraph.html",player=player,t=t)


@app.route('/matrix/<player>/<t>',methods=['POST','GET'])
def corelPlayer(player,t):
	flag=True
	l=[]
	a={"nodes":[],"links":[]}
	if request.method == 'POST':
		flag=False
		t=0.5
		name= request.get_json(force=True)
		print(name)
		if(float(name["t"])>0):
			t=float(name["t"])
		if len(name)!=0:
			
			for p in name["players"]:
				print(p)
				p=getDBname(p)
				if p in m.DBs["all"].players:
					for g in  m.DBs["all"].players[p]:
						l.append(g)
		else:
			return "error"
	else: 
		t=float(t)
		player=getDBname(player)
		if player in m.DBs["all"].players:
			l=m.DBs["all"].players[player]
	for (i,g1) in enumerate(l):
		e=event(g1.path)
		if flag:
			a["nodes"].append({"name":g1.player2+"("+g1.race2+")","group":e,"event":str(EVENT[e])})
		else:
			print("hererer")
			a["nodes"].append({"name":g1.player1,"group":g1.player1,"event":str(EVENT[e])})
	for (i,g1) in enumerate(l):
		
		for (j,g2) in enumerate(l):
			(dh,dg,da)=getAllScore(g1,g2)
			if dh<t:		
				a["links"].append({"source":i,"target":j,"value":2-dh})
	return jsonify(a)
	return "error"

@app.route("/echo", methods=['POST'])
def echo(): 
    return "You said: " + request.form['text'] 

def displayResultGuess(res1,g1):
	ret_string=""
	ret_string+="\nPlayer {0}({1}) in replay{2}:\n".format(g1.name_in_replay1,g1.race1,g1.path)
	
	for i in range(min(5,len(res1))):
		ret_string+="Guess number {0} as {1} with value {2}|{4}({5})vs{6}({7}) the {8} on {9} from file {3}\n".format(
		i+1,res1[i][2].player1,
		round(res1[i][1],2),
		res1[i][2].path,
		res1[i][2].player1,
		res1[i][2].race1,
		res1[i][2].player2,
		res1[i][2].race2,
		res1[i][2].date,
		res1[i][2].mapsc2
		)
	ret_string+="------------------------------------------\n"

	return ret_string
def getDBname(playername):
		if playername=="Hero(CJ)":
			return "hero(CJ)"
		elif playername=="HerO(Liquid)":
			return "HerO(Liquid)"
		else:
			return playername.lower()
def probaarrache(x):
	if x<=0.8:
		return ( 95+5*((-1*x/0.8+1)*(-1*x/0.8+1) )	)
	elif x<=1:
		return (90+5*( (-5*x+5)*(-5*x+5) ))
	elif x<=1.25:
		return (30 + 60*(-4*x+5)*(-4*x+5))+1
	elif x<=2:
		return (30*(-4*x+8)*(-4*x+8)/9)+1
	else:
		return 2/x 
def getNumber(player,path):
	if player in m.DBs["all"].players:
		for g in range(len(m.DBs["all"].players[player])):
			if m.DBs["all"].players[player][g].path==path:
				return g
	return "not found"
def getAllScore(g1,g2):
	E=estimator.PPVEstimator()
	d_hotkey=E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=1,coefGap=0,coefApm=0,coefFreq=0)
	d_gap=E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=0,coefGap=4,coefApm=0,coefFreq=0)
	d_apm=E.score(g1,g2,method="manhattan",option=1,maxgap=15,coefMat=0,coefGap=0,coefApm=1,coefFreq=0)
	return(d_hotkey,d_gap,d_apm)
@app.route('/analyse_replay', methods=['GET', 'POST'])
def analyse():
	a = request.form["file-uploaded"]
	print("analyse replay",a)
	print("is in dict", a in dict_of_result)
	#return "analyse replay "+str(a)
	if a in dict_of_result:
		(res1,res2,g1,g2)=dict_of_result[a]
	else:
		return "error"
	guess1=[]
	value1=[]
	guess2=[]
	value2=[]
	path1=[]
	path2=[]
	number1=[]
	number2=[]
	for i in range(3):
		(dh,dg,da)=getAllScore(g1,res1[i][2])
		guess1.append(res1[i][2].player1)
		(dh,dg,da)=getAllScore(g1,res1[i][2])
		value1.append( (round(probaarrache(res1[i][1]),2),round(dh,2),round(dg,2),round(da,2)))	
		guess2.append(res2[i][2].player1)
		(dh,dg,da)=getAllScore(g2,res2[i][2])
		value2.append(( round(probaarrache(res2[i][1]),2) ,round(dh,2),round(dg,2),round(da,2)))
		path1.append(res1[i][2].path[15:-12])
		path2.append(res2[i][2].path[15:-12])
		number1.append( getNumber(res1[i][2].player1,res1[i][2].path))
		number2.append( getNumber(res2[i][2].player1,res2[i][2].path))
		
		
		
	return render_template('analyze.html',
			nameinreplay1=g1.name_in_replay1,
			nameinreplay2=g2.name_in_replay1,
			race1=g1.race1,
			race2=g2.race1,
			guess1=guess1,
			guess2=guess2,
			value1=value1,
			value2=value2,
			path1=path1,
			path2=path2,
			number1=number1,
			number2=number2,
			filename=a
			
			)
		
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	
	if request.method == 'POST':
		file = request.files['sc2replay']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			if filename not in dict_of_result:
				(res1,res2,g1,g2)=m.guessReplay(os.path.join(app.config['UPLOAD_FOLDER'], filename),"all",coefMat=1,coefGap=4,coefApm=0,coefFreq=0)
				if(res1=="error"):
					return "error"
				
				dict_of_result[filename]=(res1,res2,g1,g2)
				#return str(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
			return filename
		else:
			return "extension error"
	
@app.route("/liste_of_player")
def liste():
	d=m.DBs["all"].players
	l=[]
	l2=[]
	gamesnumber={}
	number=[]
	for p in d:
		p2=p[0].upper()+p[1:]
		l.append(p2)
		gamesnumber[p2]=len(d[p])
		#l.append((p2,len(d[p])))
	l.sort()
	for i in l:
		l2.append((i,gamesnumber[i] ))	
	return render_template("liste_of_player.html",liste=l2)

@app.route('/player/<playername>')
def player(playername):
	
	playername2=getDBname(playername)
	list_of_number=[]
	list_of_path_of_games=[]
	list_of_player1=[]
	list_of_race1=[]
	list_of_player2=[]
	list_of_race2=[]
	list_of_dates=[]
	list_of_event=[]
	list_of_eventurl=[]
	
	#create auto corelation png

	imagename="auto"+playername+".png"
	
	if not os.path.exists(path_abs+"static/img/corelation/"+imagename):
		c=corelation.corelation()
		db1=m.DBs["all"]
		(mat,listeg1,listeg2)=c.corelation(db1,playername2,db1,playername2,coefMat=1,coefGap=0,coefApm=0,coefFreq=0)
		imagename=c.VisualizeMatrix(mat,listeg1,listeg2,display=False,groupbyname=False,path=path_abs+"static/img/corelation/",name="auto"+playername+".png")
		print (imagename)
	num=-1	
	for i in m.DBs["all"].players[getDBname(playername)]:
		num+=1
		list_of_number.append(num)
	#	list_of_games.append(num)
		list_of_player1.append(i.player1)
		list_of_race1.append(i.race1)
		list_of_player2.append(i.player2)
		list_of_race2.append(i.race2)
		list_of_dates.append(i.date)
		list_of_event.append(EVENT[event(i.path)])
		list_of_eventurl.append(EventUrl[event(i.path)])
		list_of_path_of_games.append(i.path[18:-12])
		

	path="img/corelation/"
	return render_template("player.html",name=playername,liste_path_games=list_of_path_of_games,img_corel=path+imagename,
	number=list_of_number,
	player1=list_of_player1,
	player2=list_of_player2,
	race1=list_of_race1,
	race2=list_of_race2,
	event=list_of_event,
	eventurl=list_of_eventurl,
	date=list_of_dates
	)
@app.route('/replays/<player>/<db>/<number>'	)
def replayinfo(player,db,number):
	playerDB=getDBname(player)
	number=int(number)
	if (db in m.DBs):
		print(player,db,number)
		if (playerDB in m.DBs[db].players):
			if len(m.DBs[db].players[playerDB])>=number:
				g=m.DBs[db].players[playerDB][number]
				return render_template("info_replay.html",
				p1=g.player1,
				p2=g.player2,
				race1=g.race1,
				race2=g.race2,
				path=g.path,
				eventurl=EventUrl[event(g.path)],
				event=EVENT[event(g.path)],
				name_in_replay1=g.name_in_replay1,
				name_in_replay2=g.name_in_replay2
				)
	return "404 biatch"
@app.route('/')	
def main():
	return render_template('index.html')
	
@app.route('/contacts')	
def contact():
	return render_template('contacts.html')
@app.route('/FAQ')	
def faq():
	return render_template('FAQ.html')
@app.route("/compare/<filename>/<n>/<player>")
def compare(filename,n,player):
	#we need to compute one replay against all of a player
	#we need the info on the filename and the player
	n=int(n)
	if filename in dict_of_result:
		if n==0 or n==1:
			gprout=dict_of_result[filename][2+n]
		else:
			return "error bad number"
	else:
		return "error bad filename"
	data1=[]
	data2=[]
	data3=[]
	match=-1
	if player in m.DBs["all"].players:
		n=len(m.DBs["all"].players[player])
		for g2 in m.DBs["all"].players[player]:
			
			(dh,dg,da)=getAllScore(gprout,g2)
			data1.append(dh)
			data2.append(dg)
			data3.append(da)
			mini=100
		for i in range(len(data1)):
			if(data1[i]+data2[i]<mini):
				mini=data1[i]+data2[i]
				match=i
	return render_template("testviz.html",n=n,data1=data1,data2=data2,data3=data3,match=match,name=player)


    
if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0')  
#	app.run(debug=True,host='0.0.0.0')  



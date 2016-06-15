import sys,os,hashlib
from flask import Flask, render_template, request,redirect, url_for,jsonify
from werkzeug import secure_filename
import pickle
path_abs=os.path.abspath(".")+"/"
if path_abs=="/home/sc2guess/":
		path_abs="/home/sc2guess/sc2-guessplayer/web/flaskapp/"
sys.path.insert(0, path_abs+'/../../src')
from divers import *
import corelation
import estimator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = path_abs+"replayuploaded"
app.config['MAX_CONTENT_LENGTH'] = 0.5 * 1024 * 1024

##some global value
#m=pickle.load(open(path_abs+"../../save/dbserver","rb"))
m=pickle.load(open(path_abs+"../../save/dbservertestnewreplayp3","rb"))
dict_of_result={}
liste_player=[]
for i in m.DBs["all"].players:
	liste_player.append(i)

def getNumber(player,path):
	if player in m.DBs["all"].players:
		for g in range(len(m.DBs["all"].players[player])):
			if m.DBs["all"].players[player][g].path==path:
				return g
	return "not found"

@app.route('/complexsearch')
def complex():
	return render_template("complexguess.html")

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
			a["nodes"].append({"name":g1.player2+"("+g1.race2+")","group":e,"event":str(EVENT[e]),"path":g1.path})
		else:
			a["nodes"].append({"name":g1.player1,"group":g1.player1,"event":str(EVENT[e]),"path":g1.path})
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


@app.route('/analyse_replay', methods=['GET', 'POST'])
def analyse():
	a = request.form["file-uploaded"]
	print("analyse replay",a)
	print("is in dict", a in dict_of_result)
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
	if len(res1)==0:
		return "not enough data"
	print("res1",res1,len(res1))
	for i in range(min(len(res1),3)):
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
			filename=a,
			max_=min(3,len(res1))
			
			)
		
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	print("DBS",m.DBs)
	if "userReplay" in m.DBs:
		print(m.DBs["userReplay"].players)
	db="all"
	coefMat=1
	coefGap=4
	coefApm=0
	if request.method == 'POST':
		file = request.files['sc2replay']
		
		if request.form!={}:
	
			if request.form['database']!="all":
				if "userReplay" in m.DBs:
					db="userReplay"
			coefMat=0
			coefGap=0
			coefApm=0
			if request.form['features']=="dh":
				coefMat=1
			if request.form['features']=="dg":
				coefGap=4
			if request.form['features']=="da":
				coefApm=1
					
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			full_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(full_path)
			hash_=(hashlib.md5(open(full_path, 'rb').read()).hexdigest())
			print(hash_)
			if hash_ not in dict_of_result:
				(res1,res2,g1,g2)=m.guessReplay(os.path.join(app.config['UPLOAD_FOLDER'], filename),db,coefMat=coefMat,coefGap=coefGap,coefApm=coefApm,coefFreq=0)
				if(res1=="error"):
					return "error"
				dict_of_result[hash_+db]=(res1,res2,g1,g2)
			return hash_+db
		else:
			print("erroe ex")
			return "extension error"
	
@app.route("/liste_of_player/<db>")
def liste(db):
	if db not in m.DBs:
		d=m.DBs["all"].players
	else:
		d=m.DBs[db].players
	l=[]
	l2=[]
	gamesnumber={}
	number=[]
	for p in d:
		p2=p[0].upper()+p[1:]
		l.append(p2)
		gamesnumber[p2]=len(d[p])
	#l.sort()
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


 
@app.errorhandler(413)
def page_not_found(error):
    return render_template('maxsize.html')  
     
if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')  
#	app.run(debug=True,host='0.0.0.0')  



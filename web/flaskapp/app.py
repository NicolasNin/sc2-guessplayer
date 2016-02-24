import sys,os
from flask import Flask, render_template, request,redirect, url_for
from werkzeug import secure_filename
import pickle
import sys
sys.path.insert(0, '../../src')
import corelation

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "replayuploaded"
ALLOWED_EXTENSIONS = set(["sc2replay"])

m=pickle.load(open("../../save/dbserver","rb"))

"""
sys.path.insert(0, '/home/sc2guess/sc2-guessplayer/src')




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/sc2guess/sc2-guessplayer/web/flaskapp/replayuploaded"
ALLOWED_EXTENSIONS = set(["SC2Replay"])

m=pickle.load(open("/home/sc2guess/sc2-guessplayer/save/dbserver","rb"))
"""

dict_of_result={}
def allowed_file(filename):
    return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

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
	
	for i in range(3):
		guess1.append(res1[i][2].player1)
		print(round( probaarrache(res1[i][1]) ,2),res1[i][1])

		value1.append(round( probaarrache(res1[i][1]) ,2))
		guess2.append(res2[i][2].player1)
		print(round( probaarrache(res2[i][1]) ,2),res2[i][1])
		value2.append(round(probaarrache(res2[i][1]),2))
		path1.append(res1[i][2].path[15:-12])
		path2.append(res2[i][2].path[15:-12])
		
		
	return render_template('newretour.html',
			nameinreplay1=g1.name_in_replay1,
			nameinreplay2=g2.name_in_replay1,
			race1=g1.race1,
			race2=g2.race1,
			guess1=guess1,
			guess2=guess2,
			value1=value1,
			value2=value2,
			path1=path1,
			path2=path2
			
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
	print("aa",playername,playername2)
	list_of_number=[]
	list_of_path_of_games=[]
	list_of_player1=[]
	list_of_race1=[]
	list_of_player2=[]
	list_of_race2=[]
	list_of_dates=[]
	list_of_event=[]
	
	c=corelation.corelation()
	#create auto corelation png
	db1=m.DBs["all"]
	(mat,listeg1,listeg2)=c.corelation(db1,playername2,db1,playername2,coefMat=1,coefGap=0,coefApm=0,coefFreq=0)
	path="static/img/corelation/"
	imagename=c.VisualizeMatrix(mat,listeg1,listeg2,display=False,groupbyname=False,path=path)
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
		if(i.path[18:18+3]=="WCS"):	
			list_of_event.append(i.path[18:18+16])
		else:
			list_of_event.append(i.path[18:18+3])
		list_of_path_of_games.append(i.path[18:-12])
		
	import os
	print("ici",os.getcwd())
	return render_template("player.html",name=playername,liste_path_games=list_of_path_of_games,img_corel="../../"+path+imagename,
	number=list_of_number,
	player1=list_of_player1,
	player2=list_of_player2,
	race1=list_of_race2,
	race2=list_of_race2,
	event=list_of_event,
	date=list_of_dates
	)		
@app.route("/")
def main():
	
	
	return render_template('id.html')

    
if __name__ == "__main__":
	app.run(debug=True)  
#	app.run(debug=True,host='0.0.0.0')  



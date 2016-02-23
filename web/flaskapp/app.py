import sys,os
from flask import Flask, render_template, request,redirect, url_for
from werkzeug import secure_filename
import pickle
import sys
sys.path.insert(0, '../../src')




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "replayuploaded"
ALLOWED_EXTENSIONS = set(["SC2Replay"])

m=pickle.load(open("../../save/db","rb"))
dict_of_result={}
def allowed_file(filename):
    return '.' in filename and \
			filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
		value1.append(round(res1[i][1],2))
		guess2.append(res2[i][2].player1)
		value2.append(round(res2[i][1],2))
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
	print("test upload")
	if request.method == 'POST':
		file = request.files['sc2replay']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			if filename not in dict_of_result:
				(res1,res2,g1,g2)=m.guessReplay(os.path.join(app.config['UPLOAD_FOLDER'], filename),"all",coefMat=1,coefGap=4)
				
				dict_of_result[filename]=(res1,res2,g1,g2)
				#return str(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
			return filename
		else:
			return "error with the file"
	"""
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			(res1,res2,g1,g2)=m.guessReplay(os.path.join(app.config['UPLOAD_FOLDER'], filename),"all",coefMat=1,coefGap=4)
			#html_to_display=displayResultGuess(res1,g1)
			#html_to_display+=displayResultGuess(res2,g2)
			
			#return str(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
			return render_template('retourguess.html',
			nameinreplay1=g1.name_in_replay1,
			nameinreplay2=g2.name_in_replay1,
			race1=g1.race1,
			race2=g2.race1,
			guess10=res1[0][2].player1,
			guess20=res2[0][2].player1,
			value10=round(res1[0][1],2),
			value20=round(res2[0][1],2)
			
			)
		else:
			return "file not good"
	"""			
@app.route("/liste_of_player")
def liste():
	d=m.DBs["all"].players
	l=[]
	l2=[]
	number=[]
	for p in d:
		p2=p[0].upper()+p[1:]
		l.append(p2)
		#l.append((p2,len(d[p])))
	l.sort()
	for i in l:
		l2.append((i,len(d[i.lower()])))	
	return render_template("liste_of_player.html",liste=l2)

@app.route('/player/<playername>')
def player(playername):
	list_of_games=[]
	for i in m.DBs["all"].players[playername.lower()]:
		list_of_games.append(i.path[19:-12])
	return render_template("player.html",name=playername,liste_games=list_of_games)		
@app.route("/")
def main():
	
	
	return render_template('id.html')
#	return '<form action="/echo" method="GET"><input name="text"><input type="submit" value="Echo"></form>'
	#return "Welcome!"
    
if __name__ == "__main__":
	app.run(debug=True)  
#	app.run(debug=True,host='0.0.0.0')  



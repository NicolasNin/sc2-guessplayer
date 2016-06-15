import sys,os
from flask import Flask, render_template, request,redirect, url_for,jsonify
from werkzeug import secure_filename
import corelation
import estimator


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

def getAllScore(g1,g2):
	E=estimator.PPVEstimator()
	d_hotkey=E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=1,coefGap=0,coefApm=0,coefFreq=0)
	d_gap=E.score(g1,g2,method="manhattan",option=2,maxgap=15,coefMat=0,coefGap=4,coefApm=0,coefFreq=0)
	d_apm=E.score(g1,g2,method="manhattan",option=1,maxgap=15,coefMat=0,coefGap=0,coefApm=1,coefFreq=0)
	return(d_hotkey,d_gap,d_apm)
			
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

EVENT=["Unknwown","WCS15S1","WCS15S2","WCS15S3","NW3","HS12","DH"]
EventUrl=["","http://wiki.teamliquid.net/starcraft2/2015_WCS_Season_1/",
"http://wiki.teamliquid.net/starcraft2/2015_WCS_Season_2",
"http://wiki.teamliquid.net/starcraft2/2015_WCS_Season_3",
"http://wiki.teamliquid.net/starcraft2/NationWars_III",
"http://wiki.teamliquid.net/starcraft2/HomeStory_Cup/12",
"http://wiki.teamliquid.net/starcraft2/2016_DreamHack_Open/Leipzig"]


ALLOWED_EXTENSIONS = set(["sc2replay"])
def allowed_file(filename):
    return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

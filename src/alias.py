#sc2-guessplayer
#alias of players

#problem with hero herO and bunny kr bunny eu
alias=[['forgg','m\xc7\x82forgg','millforgg',"millsymbolforgg","mforgg"],
['tlo','liquidtlo'],
['mana','liquidmana'],
['hyun','roccathyun'],
['marinelord','millmlord'],
['yoefwvanilla','fwvanilla'],
['fwslam','yoefwslam'],
['ret','liquidret'],
['toodming','toodmingcn','zootoodming',"whaletail","zoowhaletail"],
['has','fwhas'],
['macsed','igmacsed'],
['snute','liquidsnute'],
['polt','cmstormpolt'],
['xigua','igxigua'],
['san','yoefwsan'],
['taeja','liquidtaeja'],
['jaedong','egjd'],
['jim','igjim'],
["iasonu","igia","igiaprime"],
["creator","creatorprime"],
["bunny","liquidbunny"],
["harstem","fnticharstem"],
["mystery","jieshi"],
["blaze","panic"],
["bly","acerbly"],
["hear","axheart"],
["scarlett","shura"],
["jim","igjimprime"],
["neeb","neeblet"],
["qxc","colqxc"],
["demuslim","egdemuslim"],
["demuslim","egdemuslim"],
["nerchio","acernerchio"],
["puck","mellow"],
["major","light","windy","altaria","shofu"],
["scarlett","shura"],
["parting","fwparting"],
["nice","fwnice"],
["kas","empirekas","fearless"],
["stephano","mdstephano",],


]


def get(name):
	if name.lower()=="hero":
		if name[0]=="H":
			return 'HerO(Liquid)'
		else:
			return "hero(CJ)"
	name=name.lower()
	for i in alias:
		for j in i:
			if name==j:
				return i[0]
	return name

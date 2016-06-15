#sc2-guessplayer
#alias of players

#problem with hero herO and bunny kr bunny eu
alias=[['forgg'],
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
["harstem","fnticharstem","steisjo"],
["mystery","jieshi"],
["blaze","panic"],
["bly","acerbly"],
["heart","axheart"],
["scarlett","shura"],
["jim","igjimprime"],
["neeb","neeblet"],
["qxc","colqxc"],
["demuslim","egdemuslim"],
["nerchio","acernerchio"],
["puck","mellow","shloopy"],
["major","light","windy","altaria","shofu"],
["scarlett","shura"],
["parting","fwparting"],
["nice","fwnice"],
["kas","empirekas","fearless"],
["stephano","mdstephano"], #barcode from NW3 and HS12
["rogue","savage"],
["mma","acermma"],
["mvp","immvp"],
["nestea","imnestea"],
["alicia","axalicia"],
["slivko","steelmaker","vpbenqslivko:"],
["courage","zoocourage","colourdfirst","nostalie"],
["oz","pkdoz"],
["zhugeliang","wallfacer"],
["erik","olk"],
["nestea","aloola"],
["cheetos","tot"],
["iasonu", "igiasonu"],
["violet", "envyusviolet"],
["probe","nopinsea"]

]

barcode={
"IIIIIIIIIIII":["State","GosuDark"],
"IlIlIlIlIlIl":["BoomBox"] ,
"IlIlllIIl":["Stephano"] ,
"lIIlllllIIII":["Huk"],
"lIlIlIlIlIlI":["SortOf"],
"llllllllllll":["Lilbow","iaguz"],
"IlIlIlIlIlI":["Has"]
}

def get(name):
	#if name in barcode:
	#	name=barcode[name][0]
	if name.lower()=="hero" or name.lower()=="liquidhero":
		if name[0]=="H" or name[0].lower()=="l":
			return 'HerO(Liquid)'
		else:
			return "hero(CJ)"
	name=name.lower()
	for i in alias:
		for j in i:
			if name==j:
				return i[0]
	return name

#sc2-guessplayer
#alias of players

alias=[['forgg','m\xc7\x82forgg','millforgg'],
['tlo','liquidtlo'],
['mana','liquidmana'],
['hyun','roccathyun'],
['marinelord','millmlord'],
['yoefwvanilla','fwvanilla'],
['fwslam','yoefwslam'],
['ret','liquidret'],
['toodmingcn','zootoodming'],
['has','fwhas'],
['macsed','igmacsed'],
['snute','liquidsnute'],
['polt','cmstormpolt'],
['xigua','igxigua'],
['san','yoefwsan'],
['taeja','liquidtaeja'],
['jaedong','egjd'],
['jim','igjim'],
["iasonu","igia","igiaprime"]
]

def get(name):
	name=name.lower()
	for i in alias:
		for j in i:
			if name==j:
				return i[0]
	return name

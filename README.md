
What is sc2GuessPlayer?
====================
Sc2GuessPlayer is a machine learning project to find the names of the players of a starcraft 2 replay.

It is currently in early development, but achieve around 95% of success depending on which replays databases is taken as a references, and how much time there is between the two database. 

How does It work?
====================
The pro player each have their hotkeys pattern. Being given a replay It compares the features of this replay to the one in a database of reference. It is a simple classification problem, where classes are the players.
For now the best results are obtained through a closest neigbours method, which is sad but understandable. I'm far from an expert in ML and it should be possible to obtain better result through more sophisticated methods.

Will it break the meta and brings balance to the ladder ?
=======================
One can hope :D



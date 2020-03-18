import requests
import os


challenges = []
players = {}
players_sorted = []


f = open("list.csv", "r")
html_file = open("scores.html", "w")

def write_file(string):
	html_file.write(string + "\n")

for line in f: 
	tokens = line.split(";")
	if len(tokens) != 2:
		print("ERROR on line %s" % line)
		os.exit(1)
	date = tokens[0]
	challenge_id = tokens[1].strip()
	challenge = { "date" : date, "challenge_id" : challenge_id }
	challenge
	resp = requests.get("https://www.geoguessr.com/api/v3/results/scores/%s/0/100" % challenge_id)
	challenge["players"]={}
	r = resp.json()
	for player in r:
		challenge["players"][player["playerName"]] = player["totalScore"]
		players[player["playerName"]] = players.get(player["playerName"], 0) + player["totalScore"]
	challenges.append(challenge)
players_sorted = sorted(players.items(), key=lambda x: x[1], reverse=True)
f.close()

write_file("<html>")
write_file("<head>")
write_file('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
write_file('</head>')
write_file("<body>")
write_file("<table border=1>")
write_file("<tr><th> # </th>")
for chal in challenges:
	write_file('<th><a href="https://www.geoguessr.com/challenge/%s"/>%s</a></th>' % (chal["challenge_id"],chal["date"]))
write_file("<th>Total</th>")
write_file("</tr>")
for player in players_sorted:
	write_file("<tr>")
	write_file("<td>%s</td>" % player[0])
	i=0
	for challenge in challenges:
		write_file("<td>%s</td>" % challenges[i]["players"].get(player[0],""))
		i+=1
	write_file("<td>%s</td>" % player[1])
	write_file("</tr>")
write_file("</table>")
write_file("</body>")	
write_file("</html>")	

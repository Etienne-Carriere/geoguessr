import requests
import os

challenges={}
players = {}
players_sorted = []

f = open("list.csv", "r")
html_file = open("scores.html", "w")

def write_file(string):
	html_file.write(string + "\n")

for line in f: 
	tokens = line.split(";")
	if len(tokens) != 3:
		print("ERROR on line %s" % line)
		os.exit(1)
	week = tokens[0]
	date = tokens[1]
	challenge_id = tokens[2].strip()
	challenge = { "date" : date, "challenge_id" : challenge_id }
	resp = requests.get("https://www.geoguessr.com/api/v3/results/scores/%s/0/100" % challenge_id)
	challenge["players"]={}
	r = resp.json()
	for player in r:
		challenge["players"][player["playerName"]] = player["totalScore"]
		if week in players:
			players[week][player["playerName"]] = players[week].get(player["playerName"], 0) + player["totalScore"]
		else:
			players[week] = { player["playerName"] : player["totalScore"] }
	if week in challenges:
		challenges[week].append(challenge)
	else:
		challenges[week] = [ challenge ]
f.close()

write_file("<html>")
write_file("<head>")
write_file('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
write_file('</head>')
write_file("<body>")
for week,cweek in challenges.items():
	write_file("<table border=1>")
	write_file("<tr><th> # </th>")
	for chal in cweek:
		write_file('<th><a href="https://www.geoguessr.com/challenge/%s"/>%s</a></th>' % (chal["challenge_id"],chal["date"]))
	write_file("<th>Total</th>")
	write_file("</tr>")
	players_sorted = sorted(players[week].items(), key=lambda x: x[1], reverse=True)
	for player in players_sorted:
		write_file("<tr>")
		write_file("<td>%s</td>" % player[0])
		i=0
		for challenge in cweek:
			write_file("<td>%s</td>" % cweek[i]["players"].get(player[0],""))
			i+=1
		write_file("<td>%s</td>" % player[1])
		write_file("</tr>")
	write_file("</table>")
write_file("</body>")	
write_file("</html>")	

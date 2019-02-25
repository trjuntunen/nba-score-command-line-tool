import requests
import json
from datetime import datetime
from sty import fg, bg, ef, rs

def main():
	url = "http://data.nba.net/10s/prod/v1/"
	date = datetime.today().strftime('%Y-%m-%d')
	year = date[:4]
	month = date[5:7]
	day = date[8:10]
	url += year + month + day
	url += "/scoreboard.json"
	results = requests.get(url).json()
	print_results(results)

def print_results(results):
	unformatted_date = datetime.strptime(results["_internal"]["pubDateTime"][:19], '%Y-%m-%d %H:%M:%S')
	date = unformatted_date.strftime('%m/%d/%Y')
	print(fg.cyan + "NBA Games for",date + ":\n" + fg.rs)
	for game in results["games"]:

		h_team = game["hTeam"]
		a_team = game["vTeam"]
		h_team_code = h_team["triCode"]
		a_team_code = a_team["triCode"]
		game_duration = game["gameDuration"]

		if game_duration["hours"] == "" or game_duration["minutes"] == "" or game_duration["minutes"] == "00":
			print(h_team_code,"vs.",a_team_code,"@",game["startTimeEastern"],"\n")
		else:
			quarter = game["period"]["current"]
			if quarter >= 4 and not game["isGameActivated"]:
				print(fg.red + "FINAL" + fg.rs)
				print(h_team_code + ":",h_team["score"])
				print(a_team_code + ":",a_team["score"])
				if game["nugget"]["text"] != "":
					print("--------------------")
					print(game["nugget"]["text"])
				print("\n")
			else:
				print(fg.green + "Q" + str(quarter),game["clock"] + fg.rs)
				print(h_team_code + ":",h_team["score"])
				print(a_team_code + ":",a_team["score"])
				if game["nugget"]["text"] != "":
					print(game["nugget"]["text"])
				print("\n")
			

if __name__ == "__main__":
	main()

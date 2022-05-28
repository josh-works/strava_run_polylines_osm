import requests
import os
import sys
import csv
# 
token = "c503b4ce3c1aae5f42db98d9c9c3438ffc94c1ec"
# token = os.environ["STRAVA_TOKEN"]
headers = {'Authorization': "Bearer {0}".format(token)}

with open("runs.csv", "w") as runs_file:
    print("here's the token and headers")
    print(token)
    print(headers)
    writer = csv.writer(runs_file, delimiter=",")
    writer.writerow(["id", "polyline"])

    page = 1
    while True:
        r = requests.get("https://www.strava.com/api/v3/athlete/activities?page={0}".format(page), headers = headers)
        print("it's true! We're on to the next page!")
        response = r.json()

        if len(response) == 0:
            break
        else:
            for activity in response:
                r = requests.get("https://www.strava.com/api/v3/activities/{0}?include_all_efforts=true".format(activity["id"]), headers = headers)
                polyline = r.json()["map"]["polyline"]
                writer.writerow([activity["id"], polyline])
            page += 1
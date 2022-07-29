import requests
import os
import sys
import csv
#
token = "c3a0d565cfe30d62428c9ec5276e06fd7fbca579"
# token = os.environ["STRAVA_TOKEN"]
headers = {'Authorization': "Bearer {0}".format(token)}
print(headers)

with open("runs.csv", "a") as runs_file:
    print("here's the token and headers")
    print(token)
    print(headers)
    writer = csv.writer(runs_file, delimiter=",")
    writer.writerow(["id", "polyline"])

    page = 1
    while True:
        r = requests.get("https://www.strava.com/api/v3/athlete/activities?page={0}".format(page), headers = headers)
        print("it's true! We're on to the next page!")
        print(r)
        response = r.json()

        if len(response) == 0:
            break
        else:
            for activity in response:
                r = requests.get("https://www.strava.com/api/v3/activities/{0}?include_all_efforts=true".format(activity["id"]), headers = headers)
                polyline = r.json()["map"]["polyline"]
                print(activity["id"])

                writer.writerow([activity["id"], polyline])
            page += 1

    print("that's all, folks.")

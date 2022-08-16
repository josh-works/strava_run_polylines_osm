import requests
import os
import sys
import csv
#
token = "ea0a22f3cb4b7460fcbcfb6883750c2864f1318d"
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
    # page = 9
    # page = 1
    while True:
        r = requests.get("https://www.strava.com/api/v3/athlete/activities?page={0}".format(page), headers = headers)
        print("we got a response from https://www.strava.com/api/v3/athlete/activities?page={0}")
        print(r)
        response = r.json()

        if len(response) == 0:
            break
        else:
            for activity in response:
                print(activity)
                r = requests.get("https://www.strava.com/api/v3/activities/{0}?include_all_efforts=true".format(activity["id"]), headers = headers)
                polyline = r.json()["map"]["polyline"]
                print(activity["id"])

                writer.writerow([activity["id"], polyline])
            page += 1

    print("that's all, folks.")

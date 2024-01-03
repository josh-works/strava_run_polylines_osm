import requests
import os
import sys
import csv
#
token = "4e2fb0a141cdd1c2bb46d74369fd66cd8c43372d"
# token = os.environ["STRAVA_TOKEN"]
headers = {'Authorization': "Bearer {0}".format(token)}
print(headers)

with open("runs.csv", "a") as runs_file:
    print("here's the token and headers")
    print("token is: " + token)
    print("headers are: " + str(headers))
    writer = csv.writer(runs_file, delimiter=",")
    writer.writerow(["id", "polyline"])

    page = 4
    # page = 9
    # page = 1
    while True:
        r = requests.get("https://www.strava.com/api/v3/athlete/activities?page={0}".format(page), headers = headers)
        print("we got a response from https://www.strava.com/api/v3/athlete/activities?page={0}".format(page))
        print(r)
        response = r.json()

        if len(response) == 0:
            break
        else:
            for activity in response:
                print(response)
                print("activity: ")
                print(activity)
                r = requests.get("https://www.strava.com/api/v3/activities/{0}?include_all_efforts=true".format(activity["id"]), headers = headers)
                polyline = r.json()["map"]["polyline"]
                print(activity["id"])

                writer.writerow([activity["id"], polyline])
            page += 1

    print("that's all, folks.")

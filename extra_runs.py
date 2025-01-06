import requests
import os
import sys
import csv
#

runs_ids = []
with open("runs.csv") as runs_file:
    csv_reader = csv.reader(runs_file, delimiter=',')
    for row in csv_reader:
        if row[0] not in runs_ids:
            print("appending " + str(row[0]))
            runs_ids.append(row[0])

print("collected all ids to deduplicate...")

with open("runs.csv") as runs_file:
    csv_reader = csv.reader(runs_file, delimiter=',')
    for row in csv_reader:
        if row[0] not in runs_ids:
            runs_ids.append(row[0])

print("there are " + str(len(runs_ids)) + "rows of data")


token = sys.argv[1]
print(sys.argv)
print(token)
# token = os.environ["STRAVA_AUTH_TOKEN"]

headers = {'Authorization': "Bearer {0}".format(token)}
print(headers)

with open("runs.csv", "a") as runs_file:
    print("here's the token and headers")
    print("token is: " + token)
    print("headers are: " + str(headers))
    writer = csv.writer(runs_file, delimiter=",")
    
    # writer.writerow(["id", "type", "polyline"]) only needed on first run when CSV is empty/blank.

    page = 1
    more_runs_remaining = True
    # page = 9
    # page = 1
    while more_runs_remaining:
        r = requests.get("https://www.strava.com/api/v3/athlete/activities?page={0}".format(page), headers = headers)
        print("we got a response from https://www.strava.com/api/v3/athlete/activities?page={0}".format(page))
        print("we were on page " + str(page))
        
        response = r.json()
        print(response)

        if len(response) == 0:
            break
        else:
            for activity in response:
                id = activity["id"]
                type = activity["type"]
                name = activity["name"]
                distance = activity["distance"]
                start_time = activity["start_date"]

                if str(id) in runs_ids:
                    print("id already found on page " + str(page)+ ", skipping")
                    more_runs_remaining = False
                    break

                print("seems to be a new run on page " + str(page) + ", with an ID of " + str(id))
                print(name, distance, start_time)
                r = requests.get("https://www.strava.com/api/v3/activities/{0}?include_all_efforts=true".format(activity["id"]), headers = headers)
                polyline = r.json()["map"]["polyline"]
                print(id)
                print(polyline[0:100])
                writer.writerow([id, type, polyline])
                print("next activity...\n")
            page += 1

    print("that's all, folks.")

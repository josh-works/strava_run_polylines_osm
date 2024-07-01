from flask import Flask
from flask import request
from flask import render_template
import csv
import json

app = Flask(__name__)

@app.route('/')
def my_runs():
    latlng_param = ""
    initial_zoom_level = "15"

    if request.args.get('latlng'):
        latlng_param = str(request.args.get('latlng'))
    
    if request.args.get('zoom'):
        initial_zoom_level = str(request.args.get('zoom'))
    


    runs = []
    with open("runs.csv", "r") as runs_file:
        reader = csv.DictReader(runs_file)

        for row in reader:
            runs.append([ 
                row["type"],
                row["polyline"] 
            ])

    photos = []
    with open("pictures.csv", "r") as photos_file:
        reader = csv.DictReader(photos_file)

        for row in reader:
            photos.append([row["url"], row["latlng"]])

    return render_template("leaflet.html", 
                           runs = json.dumps(runs), 
                           latlng = latlng_param, 
                           zoom = initial_zoom_level,
                            photos = json.dumps(photos) )
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/felt')
def felt():
    latlng_param = ""
    initial_zoom_level = "15"
    if request.args.get('latlng'):
        latlng_param = str(request.args.get('latlng'))
    
    if request.args.get('zoom'):
        initial_zoom_level = str(request.args.get('zoom'))
    runs = []
    with open("runs.csv", "r") as runs_file:
        reader = csv.DictReader(runs_file)
        for row in reader:
            runs.append(row["polyline"])

    photos = []
    with open("pictures.csv", "r") as photos_file:
        reader = csv.DictReader(photos_file)
        for row in reader:
            photos.append([row["url"], row["latlng"]])

    print(photos[0])
    return render_template("felt.html", 
                           runs = json.dumps(runs), 
                           latlng = latlng_param, 
                           zoom = initial_zoom_level,
                            photos = json.dumps(photos) )


if __name__ == "__main__":
    app.run(port = 5001)

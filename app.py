from flask import Flask
from flask import request
from flask import render_template
import csv
import json

app = Flask(__name__)

@app.route('/')
def my_runs():
    latlng_param = ""
    print("app.py>my_runs")
    if request.args.get('latlng'):
        latlng_param = str(request.args.get('latlng'))
        print(latlng_param)
        print(type(latlng_param))
        print(request.args)

    runs = []
    with open("runs.csv", "r") as runs_file:
        reader = csv.DictReader(runs_file)

        for row in reader:
            runs.append(row["polyline"])

    return render_template("leaflet.html", runs = json.dumps(runs), latlng = latlng_param)
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == "__main__":
    app.run(port = 5001)

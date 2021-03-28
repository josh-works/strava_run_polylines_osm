# Goal

To render my nephew's currently-being-tracked bike route (via my GPS watch and my bike) on an OSM map layer so he can pan/drag/zoom/explore in a way very similar to google maps. 


OK, copied-and-pasted. It's been a while since I've written Python, and I've never actually made a Flask app, so I'm hoping it all runs without some hidden, subtled dependencing problem that's really obvious to experts but not me.

here's how this sounds in Ruby:

> Oh, you tried to `ruby file.rb` and got an obscure error? I know that means your $PATH is wrong, RVM. 

Ugh. 

I guess I need `pip`, installed.



I need an  API key from Strava.

[https://www.strava.com/settings/api](https://www.strava.com/settings/api)

Got it. I'll need to save it to my ENV to avoid accidentally committing it to Github:

```
> export STRAVA_TOKEN="12398q798798798uyfhjsdkan"
> echo $STRAVA_TOKEN
```

OK, update the value in `extra_runs.py`, getting close to being able to run it.

Now I'm getting:

```
> python extra_runs.py
Traceback (most recent call last):
  File "/Users/joshthompson/me/strava_run_polylines_osm/extra_runs.py", line 22, in <module>
    r = requests.get("https://www.strava.com/api/v3/activities/{0}?include_all_efforts=true".format(activity["id"]), headers = headers)
TypeError: string indices must be integers
```

Something's breaking in line 22. I bet there's an authorization error somewhere that's causing a bad datatype in the response, so the function is breaking as it tries to execute on an error message instead of a blob of JSON or whatever.

If it were ruby I'd stick a pry in it, but it's pry so I'm googling `pry breakpoint`. 

Turns out it's `breakpoint()`

add it right before the error, and:

```
> python extra_runs.py
> /Users/joshthompson/me/strava_run_polylines_osm/extra_runs.py(23)<module>()
-> r = requests.get("https://www.strava.com/api/v3/activities/{0}?include_all_efforts=true".format(activity["id"]), headers = headers)
(Pdb) activity
'message'
(Pdb) response
{'message': 'Authorization Error', 'errors': [{'resource': 'AccessToken', 'field': 'activity:read_permission', 'code': 'missing'}]}
(Pdb)
```


Ahh, reading the blog post more clearly, I can see part of what he's getting at. I copied-pasted a different (earlier) document in, I can see what he's working on.



## References

- [Leaflet: Mapping Strava runs/polylines on Open Street Map](https://markhneedham.com/blog/2017/04/29/leaflet-strava-polylines-osm/)
- [Above author's gist w/the code (python, flask, leaflet)](https://gist.github.com/mneedham/34b923beb7fd72f8fe6ee433c2b27d73)
- [](https://stackoverflow.com/questions/44913898/modulenotfounderror-no-module-named-requests)

## TILs

```p
> python extra_runs.py
# ugh, missing module. how do you install modules in python?
# what's python's version of RBENV. Pip. OK. Oh, I have pip, guess
# I don't know how to use it.
> python -m pip --version
> pip install requests
$ python -m pip install requests
```

- how to run basic python app on heroku?

```
pip install gunicorn
pip freeze > requirements.txt
```

https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0


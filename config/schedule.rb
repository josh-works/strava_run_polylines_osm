every 1.day, at: ['11:30 am', '11:30 pm'] do
  runner "StravaToken.runner_script_because_i_am_lazy"
  # gets fresh token and updates runs.csv w/fresh strava activity data in theory
end

every 1.minute do
  runner "StravaToken.runner_script_because_i_am_lazy"
end

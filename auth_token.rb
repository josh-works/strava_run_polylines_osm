require "uri"
require "net/http"

CLIENT_ID = ENV["STRAVA_CLIENT_ID"]
CLIENT_SECRET = ENV["STRAVA_CLIENT_SECRET"]
REFRESH_TOKEN = ENV["STRAVA_REFRESH_TOKEnnN"]

raise "#{CLIENT_ID}, #{CLIENT_SECRET}, or #{REFRESH_TOKEN} not found" unless CLIENT_ID && CLIENT_SECRET && REFRESH_TOKEN 

url = URI("https://www.strava.com/oauth/token?client_id=#{CLIENT_ID}&client_secret=#{CLIENT_SECRET}&refresh_token=#{REFRESH_TOKEN}&grant_type=refresh_token")

https = Net::HTTP.new(url.host, url.port)
https.use_ssl = true

request = Net::HTTP::Post.new(url)

response = https.request(request)
puts response.read_body

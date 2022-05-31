require "uri"
require "net/http"


# code = ARGF.argv.first
code = "b352b38e0060f3ea46c1f7a45782b5f484c58cfa"

url = URI("https://www.strava.com/oauth/token?client_id=63764&client_secret=2e6c5168e3b97a9c0975e5377041b8a416b4fbf8&code=#{code}&grant_type=authorization_code")

https = Net::HTTP.new(url.host, url.port)
https.use_ssl = true

request = Net::HTTP::Post.new(url)
request["Cookie"] = "_strava4_session=vkml9ms5bqs89hgkfdf79ob12qp2gujg"

response = https.request(request)
puts JSON.format(response.read_body)


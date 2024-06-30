require "uri"
require "net/http"
require 'json'


class StravaToken

  CLIENT_ID = ENV["STRAVA_CLIENT_ID"]
  CLIENT_SECRET = ENV["STRAVA_CLIENT_SECRET"]
  REFRESH_TOKEN = ENV["STRAVA_REFRESH_TOKEN"]

  def initialize
    raise "client_id or client_secret not found" unless CLIENT_ID && CLIENT_SECRET
  end

  def update
    raise "refresh token not found" unless REFRESH_TOKEN 

    url = URI("https://www.strava.com/oauth/token?client_id=#{CLIENT_ID}&client_secret=#{CLIENT_SECRET}&refresh_token=#{REFRESH_TOKEN}&grant_type=refresh_token")

    https = Net::HTTP.new(url.host, url.port)
    https.use_ssl = true

    request = Net::HTTP::Post.new(url)

    response = https.request(request)

    details = JSON.parse(response.read_body)
    access_token = details["access_token"]
    puts details
    puts "... returning: #{access_token}"
    return access_token
  end  
end

# lazy me
access_token = StravaToken.new.update

# result = `python extra_runs.py access_token`
result = exec("python extra_runs.py #{access_token}")



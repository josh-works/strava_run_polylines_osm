require 'nokogiri'
require 'net/http'
require 'uri'

uri = URI('https://www.strava.com')
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true if uri.scheme == 'https'

# # Create the HTTP request and set the cookie if you have one
# request = Net::HTTP::Post.new(uri.request_uri)
# request.set_form_data('username' => 'user', 'password' => 'pass')
# response = http.request(request)

# Save the cookie, or copy-paste the cookie your browser session is using right now (dev tools, or a cookie-related extension)
# cookie = response['Set-Cookie']
cookie = '_strava4_session=sqgni82q7u40j6fn2vk05ki5qt5j72i3'

# Use the cookie for subsequent requests
uri = URI('https://www.strava.com/activities/10381720567')
request = Net::HTTP::Get.new(uri)
request['Cookie'] = cookie
response = http.request(request)

# Now you can use Nokogiri to parse the HTML content
doc = Nokogiri::HTML(response.body)
# ... do something with the parsed document ...

doc.css('activity-summary activity-photos').each do |i|
  p i['src'] # get the S3/cloudfront URL like https://dgtzuqphqg23d.cloudfront.net/T2UNx0g6ApQAlT__qg0yoMPfcddatmUjFhJZCe6GuYw-2048x1536.jpg
  # and save it in a CSV, maybe w/a format like `activity_id, img_url, latlong`
end


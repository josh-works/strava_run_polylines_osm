require 'nokogiri'
require 'net/http'
require 'uri'
require 'cgi'
require 'watir'
require 'csv'
require 'fast-polylines'

@csv = CSV.read('runs.csv', headers: true)

def run_headless_browser(id)
  browser = Watir::Browser.new
  browser.goto("https://www.strava.com/activities/#{id}")
  doc = Nokogiri::HTML.parse(browser.html)

  puts "processing activity #{id}"

  div = doc.css('div[class^="Photos"]')
  imgs = div.first.css('img')
  puts imgs
  
  CSV.open('pictures.csv', 'a+') do |csv|
    imgs.each do |img|
      photo_url = img.attribute_nodes.first.value
      coords = ""

      row_from_csv = @csv.find { |row| row["id"] == id }
      if row_from_csv
        coords = FastPolylines.decode(row_from_csv["polyline"]).first
      end

      puts "writing to csv: " + [id,photo_url, coords].to_s
      csv << [id,photo_url, coords]
    end
  end
end


# uri = URI('https://www.strava.com/activities/10381720567')
# http = Net::HTTP.new(uri.host, uri.port)
# http.use_ssl = true if uri.scheme == 'https'
# request = Net::HTTP::Post.new(uri.request_uri)
# cookie = '_strava4_session=1doou87eak6frj7437q1cfs5d7h66sqa'
# request = Net::HTTP::Get.new(uri)
# request['Cookie'] = cookie.to_s
# response = http.request(request)
# doc = Nokogiri::HTML(response.body)
# f = File.new('output.html', 'w')
# f.write(response.body)
# puts "wrote some shit"

# ... do something with the parsed document ...

# doc.css('activity-summary activity-photos').each do |i|
#   p i['src'] # get the S3/cloudfront URL like https://dgtzuqphqg23d.cloudfront.net/T2UNx0g6ApQAlT__qg0yoMPfcddatmUjFhJZCe6GuYw-2048x1536.jpg
#   # and save it in a CSV, maybe w/a format like `activity_id, img_url, latlong`
# end
activity_ids = ["10381720567","10579076827",
                "10609349635",
                "10579076827",
                "10572911928",
                "10566890440",
                "10560952032",
                "10609349635",
                "10541779662",
                "10540809837",
              ]
activity_ids.each do |id|
  run_headless_browser(id)
  
end


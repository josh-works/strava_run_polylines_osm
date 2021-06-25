require 'sinatra'
  
get '/' do
  @runs = []
  p "reading_csv"
  read_csv
  File.read('index.html')
end

private

  def read_csv
    @read_csv ||=
        
        file = File.open('data/activities-all.json')
        puts file
        file.each do |row|
          @runs << row["polyline"]
        end    
  end


require 'sinatra'
  
get '/' do
  @runs = []
  File.read('index.html')
end


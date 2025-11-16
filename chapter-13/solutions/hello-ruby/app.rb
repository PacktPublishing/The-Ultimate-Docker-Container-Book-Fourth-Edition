require "sinatra"

set :bind, "0.0.0.0"   # listen on all interfaces inside the container
set :port, 4567        # default Sinatra port

get "/" do
  "Hello, World! (from Ruby + Sinatra)\n"

  db_pass = File.read(ENV["DB_PASSWORD_FILE"]).strip
  puts "Database password is: #{db_pass}"  # just for demo; don’t log in real apps
end
loop do
  puts "[INFO] Ruby worker heartbeat at #{Time.now}"
  $stdout.flush
  sleep 5
end

# Dojutsu-for-AI — Ruby client
# Prerequisites:
#   git clone https://github.com/Tryboy869/dojutsu-for-ai
#   cd dojutsu-for-ai && python allpath-runner.py daemon &
#
# Run: ruby client.rb
require "socket"
require "json"

SOCKET_PATH = "/tmp/allpath_runner.sock"
TIMEOUT     = 120

def dojutsu(function_name, args = [])
  socket = UNIXSocket.new(SOCKET_PATH)
  socket.write(JSON.generate(
    package:  "dojutsu-agent",
    function: function_name,
    args:     args
  ))
  socket.close_write

  buffer = +""
  buffer << socket.readpartial(65_536) while true rescue EOFError
  socket.close

  result = JSON.parse(buffer)
  raise "Dojutsu error: #{result["error"]}" if result["error"]
  result
rescue Errno::ENOENT
  raise "Daemon not running. Start with: python allpath-runner.py daemon &"
end

# ── Usage ──────────────────────────────────────────────────────────────
api_key = ENV["GROQ_API_KEY"] || raise("Set GROQ_API_KEY env var")

# Full pipeline
result = dojutsu("run", [
  "Build a Rails 8 API with Devise JWT, Sidekiq background jobs, and Redis caching",
  api_key,
  "groq"
])

puts "=== BYAKUGAN ==="
puts result["byakugan"]
puts "
=== CODE ==="
puts result["execution"]
puts "
Time: #{result["total_time"].round(1)}s"
puts "Skills: #{result["skills_used"].join(", ")}"

# Quick analysis
analysis = dojutsu("byakugan", [
  "Optimize a Rails app with N+1 queries and missing indexes",
  api_key,
  "groq"
])
puts "
Structural vision:
#{analysis["byakugan"]}"

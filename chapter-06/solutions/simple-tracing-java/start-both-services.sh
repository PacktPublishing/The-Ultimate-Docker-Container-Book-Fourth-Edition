#!/bin/bash
echo "Starting both services for distributed tracing demo..."

# Start Service2 in background
echo "Starting Service2 on port 8081..."
./gradlew :service2:bootRun &
SERVICE2_PID=$!

# Wait a moment for Service2 to start
sleep 5

# Start Service1 in background  
echo "Starting Service1 on port 8080..."
./gradlew :service1:bootRun &
SERVICE1_PID=$!

echo "Both services started!"
echo "Service1 PID: $SERVICE1_PID (port 8080)"
echo "Service2 PID: $SERVICE2_PID (port 8081)"
echo ""
echo "Test endpoints:"
echo "  curl localhost:8080/hello"
echo "  curl localhost:8080/test    # This will call service2"
echo "  curl localhost:8081/nested"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user interrupt
trap "echo 'Stopping services...'; kill $SERVICE1_PID $SERVICE2_PID 2>/dev/null; exit" INT
wait 
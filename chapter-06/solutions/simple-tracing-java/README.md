# Demo application for distributed tracing

This project demonstrates distributed tracing with OpenTelemetry and Jaeger using two Spring Boot services.

## Architecture

- **Service1** (port 8080): Main service with `/hello` and `/test` endpoints
- **Service2** (port 8081): Nested service with `/nested` endpoint
- **Distributed Call**: `/test` → calls → `/nested` (demonstrates trace propagation)

## Setup and Running

### 1. Start Jaeger
Open a terminal and run Jaeger using the Docker script:
```bash
./docker.sh
```

### 2. Start Both Services
You have several options:

**Option A: Start both services together**
```bash
./start-both-services.sh
```

**Option B: Start services individually**
```bash
# Terminal 1 - Start Service2
./start-service2.sh

# Terminal 2 - Start Service1  
./start-service1.sh
```

**Option C: Use Gradle directly**
```bash
# Terminal 1 - Start Service2
./gradlew :service2:bootRun

# Terminal 2 - Start Service1
./gradlew :service1:bootRun
```

### 3. Test the Endpoints

**Individual service endpoints:**
```bash
curl localhost:8080/hello   # Service1 - returns "Hello, OpenTelemetry!"
curl localhost:8081/nested  # Service2 - returns "Response from nested service"
```

**Distributed tracing endpoint:**
```bash
curl localhost:8080/test    # Service1 calls Service2 - demonstrates distributed tracing
```

### 4. View Traces in Jaeger

1. Open browser to `http://localhost:16686`
2. Under **Service** select `service1` or `service2`
3. Under **Operation** select the endpoint (e.g., `GET /test`, `GET /nested`)
4. Click **Find Traces**
5. Click on a trace to see the distributed call details

## Distributed Tracing Flow

When you call `curl localhost:8080/test`:

1. **Service1** receives the request at `/test` endpoint
2. **Service1** makes HTTP call to **Service2** at `/nested` endpoint  
3. **Service2** processes the request and returns response
4. **Service1** returns combined response
5. **OpenTelemetry** automatically creates a distributed trace showing the complete flow
6. **Jaeger** displays the trace with parent-child span relationships

The trace will show:
- Parent span: `GET /test` in service1
- Child span: HTTP client call from service1 to service2
- Child span: `GET /nested` in service2
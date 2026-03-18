# whoami-python

A minimal Python web service that returns information about the host it is running on — useful for testing deployments, container networking, and load balancing.

## What it returns

A JSON response containing:

- `hostname` — the container / machine hostname
- `ip` — the resolved IP address
- `platform` — the OS name (e.g. `Linux`)
- `environment` — all environment variables visible to the process

## Run locally

```bash
python app.py
```

Then open <http://localhost:8080>.

Set a custom port via the `PORT` environment variable:

```bash
PORT=9000 python app.py
```

## Run with Docker

**Build:**

```bash
docker build -t whoami-python .
```

**Run:**

```bash
docker run --rm -p 8080:8080 whoami-python
```

Then open <http://localhost:8080>.

## Example response

```json
{
  "hostname": "a1b2c3d4e5f6",
  "ip": "172.17.0.2",
  "platform": "Linux",
  "environment": {
    "PATH": "/usr/local/bin:/usr/bin:/bin",
    "PORT": "8080"
  }
}
```

## Requirements

No third-party dependencies — uses the Python standard library only.

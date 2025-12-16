# Python SDK

The `sibna` Python package is the reference implementation of the protocol.

## Installation
```bash
pip install sibna
```

## Quick Start
```python
from sibna import Client

# Initialize
alice = Client("alice")
alice.start()

# Register
alice.register()

# Send
alice.send("bob", "Hello Secret World!")
```

## API Reference
- `Client(user_id, server_url)`: Main entry point.
- `client.start()`: Starts the background network loop.
- `client.stop()`: Clean shutdown.

# Sibna Protocol Developer Guide

Welcome to the Sibna Ecosystem. This guide will help you build secure, resilient applications using the `sibna` SDK.

## 1. Installation

```bash
pip install sibna  # (Coming soon to PyPI)
# For now:
# pip install .
```

## 2. Quick Start: The "Hello World" of Secure Messaging

To send a message, you need two things: an Identity and a Server.

```python
from sibna import Client

# 1. Initialize Client
# This automatically creates a local database 'alice.db' to store your keys and messages.
client = Client("alice", server_url="http://localhost:8000")

# 2. Start the Engine
# This handles the background networking, encryption, and retry logic.
client.start()

# 3. Register on the Network
# Uploads your public keys to the server so others can find you.
client.register()

# 4. Send a Message
# If 'bob' is offline, the message waits in your local queue.
client.send("bob", "Hello! This is encrypted end-to-end.")

# 5. Stop when done
client.stop()
```

## 3. Architecture for App Developers

### The "Thick Client" Model
Sibna uses a "Thick Client" architecture. Logic lives in your app, not the server.
- **You** (the App) hold the keys.
- **You** (the App) store the messages (SQLite).
- **The Server** is just a dumb relay.

### Handling Incoming Messages
(Coming in v1.1)
```python
@client.on_message
def handle_msg(sender, payload):
    print(f"New message from {sender}: {payload}")
```

## 4. Building for Scale
- **Database**: The SDK uses SQLite by default. For mobile (Flutter/React Native), we provide bindings to the Rust Core directly.
- **Custom Servers**: You can run your own relay server (see `DEPLOYMENT.md`).

# Secure Protocol Python Bindings

A secure, multi-language communication protocol implementation.

## Features
- Double Ratchet Algorithm
- X3DH Key Agreement
- Forward Secrecy & Post-Compromise Security
- Metadata Privacy

## Installation
```bash
pip install secure-protocol
```

## Usage
```python
from secure_protocol import SecureContext, Config, RelayClient

# Initialize
ctx = SecureContext(Config())

# Connect to Relay
client = RelayClient("localhost", 5000, my_public_key)
client.connect()
```

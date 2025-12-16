# System Architecture

Sibna is designed as a distributed, client-heavy system. The intelligence lives at the edges (the clients), while the center (the server) is minimal and untrusted.

## High-Level Topology

```
[ Alice (Client) ] <---> [ Sibna Relay (Server) ] <---> [ Bob (Client) ]
      |                           |                           |
  (SQLite DB)                (SQLite DB)                 (SQLite DB)
  - PreKeys                  - Message Queue             - PreKeys
  - Sessions                 - Users Dir                 - Sessions
  - Message Log                                          - Message Log
```

## The Data Flow

### 1. Registration (Identity Creation)
1.  Alice generates a stable Identity Key Pair ($IK_a$).
2.  She generates a Signed PreKey ($SPK_a$) and a batch of One-Time PreKeys ($OPK_a^1...OPK_a^{100}$).
3.  She signs $SPK_a$ with $IK_a$.
4.  She uploads this "Key Bundle" to the Server.

### 2. Session Initialization (X3DH)
When Bob wants to talk to Alice:
1.  Bob fetches Alice's Key Bundle from the Server.
2.  Bob performs the X3DH calculation locally to derive a Shared Secret ($SK$).
3.  Bob deletes Alice's One-Time Key used in the process.
4.  Bob encrypts an initial message using $SK$ and sends it to the Server.

### 3. The Relay (Server Handling)
1.  The Server receives the encrypted blob.
2.  It looks up "Alice" in its database.
3.  It appends the blob to Alice's `inbox` table.
4.  It returns `200 OK` to Bob. (Bob now knows the server accepted it).

### 4. Delivery & Decryption
1.  Alice comes online and polls `GET /messages`.
2.  The Server sends the encrypted blob.
3.  Alice uses her private keys to replicate the X3DH math Bob did.
4.  She derives the same Shared Secret ($SK$).
5.  She decrypts the message.

## Client Architecture (SDK)

The `sibna` Client is composed of three layers:

1.  **Network Layer**: Handles HTTP retries, timeouts, and JSON serialization.
2.  **Storage Layer**: A local SQLite database managing the `outbox` (retry queue) and `sessions` (Double Ratchet properties).
3.  **Crypto Core**: The logic for X3DH and Ratcheting (implemented in Python/Rust).

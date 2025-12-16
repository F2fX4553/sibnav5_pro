# Security Model

This document outlines the threat model Sibna is designed to withstand and the guarantees it provides.

## Threat Assumptions
We assume a **powerful adversary** (e.g., a nation-state or compromised server admin) who:
1.  Can read all network traffic (Passive Surveillance).
2.  Can inject, delay, or replay network packets (Active MiTM).
3.  Has full read/write access to the Relay Server's database.
4.  Can compromise a user's device *temporarily*.

## Security Guarantees

| Property | Guarantee | Mechanism |
| :--- | :--- | :--- |
| **Confidentiality** | The adversary cannot read message content. | End-to-End Encryption (AES-256-GCM) |
| **Integrity** | Message tampering is detected. | Authenticated Encryption (GCM tag) |
| **Authenticity** | Messages strictly come from the claimed sender. | Ed25519 Signatures on Keys |
| **Forward Secrecy** | Past messages remain secure if a key is stolen. | Session Ratcheting & One-Time PreKeys |
| **PC Security** | Future messages heal the session after a breach. | Diffie-Hellman Ratchet Steps |
| **Metadata Privacy** | The server knows *who* is talking, but not *what*. | Sealed Sender (partial) / Encrypted Payloads |

## Attack Vectors & Mitigations

### 1. The "Evil Server" Attack
**Scenario**: The server admin tries to inject a fake public key for Alice to spy on Bob.
**Mitigation**: **TOFU (Trust On First Use)**. The server cannot overwrite Alice's Identity Key once established. Bob's client pins Alice's identity. If it changes, the client alerts the user.

### 2. Replay Attack
**Scenario**: An attacker captures a valid encrypted message and sends it to Alice again 100 times.
**Mitigation**: The local database tracks the `ratchet_step`. Any message with a `step <= current_step` is silently discarded as a duplicate.

### 3. Traffic Analysis
**Scenario**: Watching packet sizes to guess content (e.g., "This message is 5MB, it must be a photo").
**Mitigation**: Pad messages to fixed block sizes (future work). Currently, transport layer uses TLS (HTTPS) to mask exact byte boundaries.

# Protocol Specification v2.0

> **Warning**: This document contains heavy cryptographic details. You do not need to understand this to use the SDK.

Sibna Protocol v2 combines **X3DH** (Extended Triple Diffie-Hellman) for key agreement and the **Double Ratchet** algorithm for message encryption.

## 1. Cryptographic Primitives
- **Curve**: X25519 (Elliptic Curve Diffie-Hellman).
- **Signing**: Ed25519.
- **Cipher**: AES-256-GCM (Authenticated Encryption).
- **Hash**: SHA-256.
- **KDF**: HKDF (HMAC-based Key Derivation Function).

## 2. X3DH (Key Agreement)

To establish a session, Bob computes a master secret $SK$ using keys from Alice's bundle.

$SK = KDF( DH(IK_a, E_b) || DH(SPK_a, E_b) || DH(SPK_a, IK_b) || DH(OPK_a, IK_b) )$

Where:
- $IK$: Identity Key (Long-term)
- $SPK$: Signed PreKey (Medium-term)
- $OPK$: One-Time PreKey (One-use)
- $E$: Ephemeral Key (Generated just for this handshake)

This ensures that even if Alice's Identity Key is compromised later, the session key remains safe (Forward Secrecy via $OPK$ and $E$).

## 3. Double Ratchet (Message Encryption)

Once $SK$ is established, it is used as the "Root Key" for the Double Ratchet.

### The Symmetric Ratchet
For every message sent, the Chain Key ($CK$) rolls forward using a One-Way Function (Hash).
$$ CK_{n+1} = HMAC(CK_n, \text{"Update"}) $$
$$ MessageKey = HMAC(CK_n, \text{"Message"}) $$

This ensures that obtaining a message key reveals nothing about previous keys (Forward Secrecy).

### The Diffie-Hellman Ratchet
If users are strictly taking turns (ping-pong), we perform a DH Ratchet.
1.  Bob sends a new public key $E_{bob}$ with his message.
2.  Alice receives it, computes $DH(E_{bob}, E_{alice})$, and derives a **new Root Key**.
3.  This resets the chains.

This ensures that if a key is stolen, the attacker is locked out as soon as a new reply is sent (Post-Compromise Security).

## 4. Header Encryption
To minimize metadata leakage, the message header (containing the ratchet step number) is also encrypted. Only the intended recipient can decode *which* turn of the conversation this is.

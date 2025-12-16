from sibna import Client
import time

def main():
    print("🚀 Initializing Sibna Secure Comm...")
    
    # 1. Create a client (Identity is auto-loaded from disk)
    alice = Client("alice_prod", server_url="http://localhost:8000")
    
    # 2. Start the background engine (Networking/Encryption)
    alice.start()
    
    # 3. Register (Upload keys to server)
    alice.register()
    
    # 4. Send a secure message
    print("✉️  Sending message to Bob...")
    alice.send("bob_prod", "Hello, Bob! This is using the Sibna SDK.")
    
    # Keep alive to allow background sending
    time.sleep(2)
    
    print("✅ Message Queued and Sent (Check local logs).")
    alice.stop()

if __name__ == "__main__":
    main()

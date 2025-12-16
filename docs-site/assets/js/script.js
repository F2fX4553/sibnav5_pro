const contentMap = {
    home: `
        <div class="hero">
            <h1>The Sibna Protocol</h1>
            <p class="lead">The open-source standard for <strong>Trust-No-One</strong> communication.</p>
            <div class="metrics">
                <span>🛡️ Quantum-Ready Design</span>
                <span>⚡ &lt; 50ms Latency</span>
                <span>🌍 Cross-Platform</span>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>🔒 End-to-End Encryption</h3>
                <p>Built on the Double Ratchet algorithm. Every message has a unique ephemeral key. Forward Secrecy and Post-Compromise Security included.</p>
            </div>
            <div class="card">
                <h3>⚡ Offline-First Architecture</h3>
                <p>Messages are queued locally (SQLite) and synchronized when connectivity is restored. Perfect for unstable networks.</p>
            </div>
            <div class="card">
                <h3>🆔 Self-Sovereign Identity</h3>
                <p>No phone numbers. No emails. Just cryptographic keys. You own your identity, not the server.</p>
            </div>
        </div>

        <h2>Ecosystem Support</h2>
        <div class="grid-sm">
            <div class="chip python">Python (Core)</div>
            <div class="chip js">Node.js / React</div>
            <div class="chip dart">Flutter / Dart</div>
            <div class="chip rust">Rust (Native)</div>
        </div>
    `,
    protocol: `
        <h1>Protocol Specification v2.0</h1>
        <p>The core of Sibna is an asynchronous, stateful cryptographic session management system.</p>

        <h2>1. The Handshake (X3DH)</h2>
        <p>Before Alice can message Bob, they must agree on a shared secret key. Sibna uses Extended Triple Diffie-Hellman (X3DH) to allow this <em>asynchronously</em> (even if Bob is offline).</p>
        <ul>
            <li><strong>Identity Key ($IK$):</strong> Long-term signing key.</li>
            <li><strong>Signed PreKey ($SPK$):</strong> Medium-term encryption key, signed by $IK$.</li>
            <li><strong>One-Time PreKey ($OPK$):</strong> Single-use key for forward secrecy.</li>
        </ul>

        <h2>2. Transport Layer Security</h2>
        <p>Sibna enforces <strong>HSTS</strong> and pinning. All payloads are signed. The server (Relay) can see <em>metadata</em> (who talks to whom) but <strong>never</strong> the content.</p>
    `,
    "sdk-python": `
        <h1>Python SDK</h1>
        <p>The standard library for building Bots, CLIs, and Desktop apps.</p>
        
        <h3>1. Installation</h3>
        <pre>pip install sibna</pre>

        <h3>2. Usage (Bot Example)</h3>
        <pre><code class="language-python">from sibna import Client

# Initialize persistent client
bot = Client("support_bot", server_url="https://api.sibna.io")
bot.start()

# Register identity
bot.register()

print("Bot is listening...")
# (Event loop would go here)
</code></pre>

        <h3>3. Advanced: Key Management</h3>
        <p>Keys are stored in <code>user_id_storage.db</code> using SQLite. You can back this file up to restore your account.</p>
    `,
    "sdk-js": `
        <h1>JavaScript SDK (React / Vue / Next.js)</h1>
        <p>Bring secure messaging to the web using WebAssembly-powered crypto.</p>

        <h3>1. Installation</h3>
        <pre>npm install sibna-js</pre>

        <h3>2. Usage (React Hook)</h3>
        <pre><code class="language-javascript">import { useSibna } from 'sibna-js/react';

function ChatApp() {
  const client = useSibna('alice_web');

  const sendMessage = async () => {
    await client.send('bob', 'Hello from Browser!');
  };

  return &lt;button onClick={sendMessage}&gt;Send Secure&lt;/button&gt;;
}</code></pre>
    `,
    "sdk-flutter": `
        <h1>Flutter SDK (Mobile)</h1>
        <p>Native performance for iOS and Android.</p>

        <h3>1. Installation</h3>
        <pre>dependencies:
  sibna_dart: ^1.0.0</pre>

        <h3>2. Usage</h3>
        <pre><code class="language-dart">import 'package:sibna_dart/client.dart';

void main() async {
  var client = SibnaClient(userId: 'alice_mobile');
  await client.initialize();
  
  await client.send(
    recipient: 'bob', 
    content: 'Sent from my iPhone'
  );
}</code></pre>
    `,
    installation: `
        <h1>Server Deployment</h1>
        <p>Want to run your own relay? It's easy using Docker.</p>
        <pre>docker run -d -p 8000:8000 secure-server:latest</pre>
        <p>See <a href="#" onclick="alert('See DEPLOYMENT.md in repo')">DEPLOYMENT.md</a> for full details.</p>
    `,
    deployment: `
        <h1>Deployment Architecture</h1>
        <p>For high availability, we recommend:</p>
        <ul>
            <li><strong>Load Balancer:</strong> Nginx / AWS ALB</li>
            <li><strong>Compute:</strong> 2x Docker Containers (Blue/Green)</li>
            <li><strong>Storage:</strong> Managed SQLite (LiteFS) or PostgreSQL Adapter (Enterprise)</li>
        </ul>
    `
};

document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-links li[data-page]');
    const contentDiv = document.getElementById('page-content');

    function loadPage(pageId) {
        // Update Active State
        navLinks.forEach(l => l.classList.remove('active'));
        const activeLink = document.querySelector(`.nav-links li[data-page="${pageId}"]`);
        if (activeLink) activeLink.classList.add('active');

        // Inject Content
        const html = contentMap[pageId] || "<h1>404 Not Found</h1><p>Documentation in progress...</p>";
        contentDiv.innerHTML = html;
    }

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const pageId = link.getAttribute('data-page');
            loadPage(pageId);
        });
    });

    // Load Default
    loadPage('home');
});

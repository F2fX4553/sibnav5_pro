# Flutter SDK

Build native secure messenger apps for iOS and Android using `sibna-dart`.

## Installation
Add this to your `pubspec.yaml`:
```yaml
dependencies:
  sibna_dart: ^1.0.0
```

## Usage
The API mirrors the Python SDK for consistency.

```dart
final client = SibnaClient(userId: 'mobile_user');
await client.initialize();

// Send a message
await client.send(recipient: 'server_bot', content: 'Ping');

// Listen for messages
client.messages.listen((msg) {
  print('New Message: ${msg.content}');
});
```

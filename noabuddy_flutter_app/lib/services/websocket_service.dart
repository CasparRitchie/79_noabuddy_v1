import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  final String url;
  late WebSocketChannel _channel;

  WebSocketService({required this.url}) {
    _channel = WebSocketChannel.connect(Uri.parse(url));
  }

  Stream get stream => _channel.stream;

  void sendMessage(String message) {
    _channel.sink.add(message);
  }

  void closeConnection() {
    _channel.sink.close();
  }
}

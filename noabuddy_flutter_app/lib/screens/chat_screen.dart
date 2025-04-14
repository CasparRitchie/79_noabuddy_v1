import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'dart:html' as html; // 🔊 For TTS in browser
import '../services/web_recorder.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<Map<String, dynamic>> _messages = [];
  final WebRecorder _recorder = WebRecorder();
  bool _isRecording = false;
  void _speak(String text) {
  final utterance = html.SpeechSynthesisUtterance(text);
  html.window.speechSynthesis?.cancel(); // ✅ safe null-aware access
  html.window.speechSynthesis?.speak(utterance); // ✅ safe null-aware access
}


  Future<void> _startRecording() async {
    try {
      setState(() => _isRecording = true);
      await _recorder.startRecording();
    } catch (e) {
      print('🎤 Error starting recording: $e');
      setState(() {
        _isRecording = false;
        _messages.add({'text': '❌ Could not start microphone', 'isUser': false});
      });
    }
  }

  Future<void> _stopRecordingAndSend() async {
    try {
      setState(() {
        _isRecording = false;
        _messages.add({'text': '🎙️ Listening and processing...', 'isUser': false});
      });

      final audioBytes = await _recorder.stopRecording();
      print("📦 Audio byte length: ${audioBytes.length}");

      final request = http.MultipartRequest(
        'POST',
        // Uri.parse('https://f8cd-82-1-18-199.ngrok-free.app/api/speak'),
        Uri.parse('https://noabuddy-v1-a82fc408a503.herokuapp.com/api/speak'),

      );

      request.files.add(http.MultipartFile.fromBytes(
        'file',
        audioBytes,
        filename: 'speech.wav',
        contentType: MediaType('audio', 'wav'),
      ));

      final response = await request.send();
      final responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final data = json.decode(responseBody);
        final userSaid = data['transcript'] ?? '';
        final botResponse = data['response'] ?? '🤖 No reply received';

        setState(() {
          if (userSaid.isNotEmpty) {
            _messages.add({'text': userSaid, 'isUser': true});
          }
          _messages.add({'text': botResponse, 'isUser': false});
        });

        // 🔊 Speak the bot's reply aloud
        _speak(botResponse);
      } else {
        setState(() {
          _messages.add({
            'text': '⚠️ Error from backend: ${response.statusCode}',
            'isUser': false
          });
        });
      }
    } catch (e) {
      print('❌ Error sending audio: $e');
      setState(() {
        _messages.add({'text': '❌ Failed to send audio', 'isUser': false});
      });
    }
  }


  Widget _buildMessage(Map<String, dynamic> msg) {
    return Align(
      alignment: msg['isUser'] ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: msg['isUser'] ? Colors.teal.shade100 : Colors.grey.shade200,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(msg['text']),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("NoaBuddy")),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              reverse: false,
              itemCount: _messages.length,
              itemBuilder: (context, index) => _buildMessage(_messages[index]),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Row(
              children: [
                IconButton(
                  icon: Icon(_isRecording ? Icons.stop : Icons.mic),
                  onPressed: _isRecording ? _stopRecordingAndSend : _startRecording,
                ),
                const SizedBox(width: 8),
                const Text("Tap to speak"),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

import 'package:flutter/material.dart';

class InputBar extends StatelessWidget {
  final TextEditingController controller;
  final void Function(String) onSend;

  const InputBar({
    Key? key,
    required this.controller,
    required this.onSend,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(8, 8, 8, 16),
        child: Row(
          children: [
            IconButton(
              icon: const Icon(Icons.mic),
              onPressed: () {
                // TODO: Add microphone input logic (Vosk or SpeechToText)
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Mic input not implemented yet')),
                );
              },
            ),
            Expanded(
              child: TextField(
                controller: controller,
                textInputAction: TextInputAction.send,
                decoration: const InputDecoration(
                  hintText: 'Type a message or say "Guidance"',
                ),
                onSubmitted: onSend,
              ),
            ),
            IconButton(
              icon: const Icon(Icons.send),
              onPressed: () {
                onSend(controller.text);
              },
            ),
            PopupMenuButton<String>(
              icon: const Icon(Icons.more_vert),
              onSelected: (value) {
                if (value == 'Guidance') {
                  onSend('Guidance');
                } else if (value == 'Quiet') {
                  onSend('Quiet');
                }
              },
              itemBuilder: (context) => const [
                PopupMenuItem(value: 'Guidance', child: Text('Guidance')),
                PopupMenuItem(value: 'Quiet', child: Text('Quiet')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

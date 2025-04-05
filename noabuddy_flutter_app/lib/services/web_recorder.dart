import 'dart:html';
import 'dart:typed_data';
import 'dart:async';

class WebRecorder {
  MediaRecorder? _recorder;
  List<Blob> _chunks = [];

  Future<void> startRecording() async {
    final stream = await window.navigator.mediaDevices?.getUserMedia({'audio': true});
    if (stream == null) throw Exception("Failed to get user microphone");

    _recorder = MediaRecorder(stream);
    _chunks = [];

    _recorder!.addEventListener('dataavailable', (event) {
      final blobEvent = event as BlobEvent;
      _chunks.add(blobEvent.data!);
    });

    _recorder!.start();
  }

  Future<Uint8List> stopRecording() async {
    final completer = Completer<Uint8List>();
    if (_recorder == null) throw Exception("Recorder not initialized");

    _recorder!.addEventListener('stop', (_) async {
      try {
        final blob = Blob(_chunks);
        final reader = FileReader();
        reader.readAsArrayBuffer(blob);
        await reader.onLoad.first;

        final result = reader.result;
          if (result is ByteBuffer) {
            completer.complete(Uint8List.view(result));
          } else if (result is Uint8List) {
            completer.complete(result);
          } else {
            completer.completeError("Unsupported audio buffer type: ${result.runtimeType}");
          }

      } catch (e) {
        completer.completeError("Failed to process recording: \$e");
      }
    });

    _recorder!.stop();
    return completer.future;
  }

  void reset() {
    _recorder = null;
    _chunks.clear();
  }
}

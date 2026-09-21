import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({super.key});

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  final _titleController = TextEditingController();
  final _opponentController = TextEditingController();
  String _matchType = 'full_match';
  bool _isUploading = false;
  double _progress = 0.0;

  Future<void> _pickVideo() async {
    final picker = ImagePicker();
    final video = await picker.pickVideo(source: ImageSource.gallery);
    if (video != null) {
      setState(() => _isUploading = true);
      // Simulate upload
      for (int i = 0; i <= 100; i += 10) {
        await Future.delayed(const Duration(milliseconds: 200));
        setState(() => _progress = i / 100);
      }
      setState(() => _isUploading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Video uploaded! Processing started.'), backgroundColor: Color(0xFF00B894)),
        );
        Navigator.pop(context);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Upload Match Video")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              height: 200,
              decoration: BoxDecoration(
                color: const Color(0xFF1D1F33),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF00B894), width: 2, style: BorderStyle.solid),
              ),
              child: Center(
                child: _isUploading
                    ? Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          CircularProgressIndicator(value: _progress, color: const Color(0xFF00B894)),
                          const SizedBox(height: 16),
                          Text("${(_progress * 100).toInt()}%", style: const TextStyle(color: Colors.white)),
                        ],
                      )
                    : Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.videocam, size: 48, color: Color(0xFF00B894)),
                          const SizedBox(height: 8),
                          const Text("Tap to select video", style: TextStyle(color: Colors.white70)),
                          const SizedBox(height: 4),
                          const Text("MP4, MOV, AVI up to 2GB", style: TextStyle(color: Colors.white38, fontSize: 12)),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 24),
            TextField(
              controller: _titleController,
              style: const TextStyle(color: Colors.white),
              decoration: _inputDecoration("Match Title", Icons.title),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _opponentController,
              style: const TextStyle(color: Colors.white),
              decoration: _inputDecoration("Opponent Team", Icons.group),
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _matchType,
              dropdownColor: const Color(0xFF1D1F33),
              style: const TextStyle(color: Colors.white),
              decoration: _inputDecoration("Match Type", Icons.sports),
              items: const [
                DropdownMenuItem(value: 'full_match', child: Text('Full Match')),
                DropdownMenuItem(value: 'highlights', child: Text('Highlights')),
                DropdownMenuItem(value: 'training', child: Text('Training Session')),
                DropdownMenuItem(value: 'trial', child: Text('Trial Match')),
              ],
              onChanged: (v) => setState(() => _matchType = v!),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: _isUploading ? null : _pickVideo,
              icon: const Icon(Icons.cloud_upload),
              label: const Text("Upload & Analyze"),
            ),
            const SizedBox(height: 16),
            const Text(
              "Your video will be processed by our AI engine. 90-minute matches are analyzed in under 4 minutes.",
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white38, fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }

  InputDecoration _inputDecoration(String label, IconData icon) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: Colors.white70),
      prefixIcon: Icon(icon, color: Colors.white70),
      filled: true,
      fillColor: const Color(0xFF1D1F33),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
    );
  }
}

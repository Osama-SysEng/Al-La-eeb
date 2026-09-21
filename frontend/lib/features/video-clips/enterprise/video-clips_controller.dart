import 'video-clips_state.dart';

class VideoClipsController {
  VideoClipsState state = const VideoClipsState();
  void beginLoad() => state = const VideoClipsState(loading: true);
  void fail(String message) => state = VideoClipsState(error: message);
}

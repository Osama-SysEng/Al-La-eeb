abstract interface class VideoClipsRepository {
  Future<List<Object>> load({String? cursor});
}

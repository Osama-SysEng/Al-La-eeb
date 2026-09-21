abstract interface class ScoutingBoardRepository {
  Future<List<Object>> load({String? cursor});
}

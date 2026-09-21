abstract interface class AnalysisQueueRepository {
  Future<List<Object>> load({String? cursor});
}

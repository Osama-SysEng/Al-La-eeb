abstract interface class PerformanceReportRepository {
  Future<List<Object>> load({String? cursor});
}

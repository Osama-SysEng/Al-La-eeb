abstract interface class DevelopmentPlanRepository {
  Future<List<Object>> load({String? cursor});
}

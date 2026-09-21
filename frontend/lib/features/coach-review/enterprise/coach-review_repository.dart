abstract interface class CoachReviewRepository {
  Future<List<Object>> load({String? cursor});
}

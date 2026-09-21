abstract interface class AthleteProfileRepository {
  Future<List<Object>> load({String? cursor});
}

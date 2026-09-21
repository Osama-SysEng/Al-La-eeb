import 'athlete-profile_state.dart';

class AthleteProfileController {
  AthleteProfileState state = const AthleteProfileState();
  void beginLoad() => state = const AthleteProfileState(loading: true);
  void fail(String message) => state = AthleteProfileState(error: message);
}

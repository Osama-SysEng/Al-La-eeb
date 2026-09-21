import 'coach-review_state.dart';

class CoachReviewController {
  CoachReviewState state = const CoachReviewState();
  void beginLoad() => state = const CoachReviewState(loading: true);
  void fail(String message) => state = CoachReviewState(error: message);
}

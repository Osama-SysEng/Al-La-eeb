import 'development-plan_state.dart';

class DevelopmentPlanController {
  DevelopmentPlanState state = const DevelopmentPlanState();
  void beginLoad() => state = const DevelopmentPlanState(loading: true);
  void fail(String message) => state = DevelopmentPlanState(error: message);
}

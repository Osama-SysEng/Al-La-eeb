import 'analysis-queue_state.dart';

class AnalysisQueueController {
  AnalysisQueueState state = const AnalysisQueueState();
  void beginLoad() => state = const AnalysisQueueState(loading: true);
  void fail(String message) => state = AnalysisQueueState(error: message);
}

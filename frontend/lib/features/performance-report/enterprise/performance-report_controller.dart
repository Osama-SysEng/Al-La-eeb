import 'performance-report_state.dart';

class PerformanceReportController {
  PerformanceReportState state = const PerformanceReportState();
  void beginLoad() => state = const PerformanceReportState(loading: true);
  void fail(String message) => state = PerformanceReportState(error: message);
}

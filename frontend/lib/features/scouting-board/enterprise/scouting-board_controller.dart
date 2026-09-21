import 'scouting-board_state.dart';

class ScoutingBoardController {
  ScoutingBoardState state = const ScoutingBoardState();
  void beginLoad() => state = const ScoutingBoardState(loading: true);
  void fail(String message) => state = ScoutingBoardState(error: message);
}

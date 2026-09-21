bool canPublishVideoClips(String action, {required bool reviewed, required bool consented}) {
  const protected = {'publish_report', 'biometric_export', 'player_comparison'};
  return consented && (!protected.contains(action) || reviewed);
}

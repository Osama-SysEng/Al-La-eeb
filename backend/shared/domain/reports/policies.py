REVIEW_ACTIONS = {"PUBLISH_REPORT", "BIOMETRIC_EXPORT", "MODEL_PROMOTION", "PLAYER_COMPARISON"}

def requires_review(action: str, consent: bool = True) -> bool:
    return action.upper() in REVIEW_ACTIONS or not consent

def may_process_video(consent: bool, retention_days: int) -> bool:
    return consent and 1 <= retention_days <= 365

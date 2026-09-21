from .contracts import VideoSnapshot

def display_label(snapshot: VideoSnapshot) -> str:
    return f"{snapshot.identifier} · {snapshot.status}"

def is_terminal(status: str) -> bool:
    return status.upper() in {"ARCHIVED", "COMPLETED", "FAILED", "RETAINED"}

import time
import random
from src.utils.logger import log_event

def backoff_retry_sleep(attempt: int):
    """
    Exponential backoff with jitter.
    attempt: 0-indexed
    """
    base = 0.5
    sleep = min(base * (2 ** attempt), 4) + random.uniform(0, 0.25)
    log_event("Planner", "backoff_sleep", {"attempt": attempt, "sleep": round(sleep, 2)})
    time.sleep(sleep)

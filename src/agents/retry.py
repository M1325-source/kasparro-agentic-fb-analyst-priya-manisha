import time
import random
import logging
from typing import Callable

log = logging.getLogger("retry")

def _is_transient_exception(exc: Exception) -> bool:
    """
    Heuristic to classify transient exceptions.
    Looks at exception class name and message for keywords.
    """
    name = exc.__class__.__name__.lower()
    msg = str(exc).lower()
    transient_kw = ["timeout", "temporar", "connection", "rate", "throttl", "transient"]
    return any(k in name or k in msg for k in transient_kw)

def retry_with_backoff(fn: Callable, attempts: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
    """
    Decorator-style helper. Example use:
      decorated = retry_with_backoff(func, attempts=4, base_delay=1.0)
      decorated(*args)
    """
    def wrapper(*args, **kwargs):
        last_exc = None
        for attempt in range(1, attempts + 1):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                last_exc = e
                transient = _is_transient_exception(e)
                # Log context
                log.warning("Attempt %d/%d failed: %s (transient=%s)", attempt, attempts, e, transient)
                if attempt == attempts and not transient:
                    # final non-transient error -> raise immediately
                    raise
                # compute backoff (exponential) + jitter
                delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
                jitter = random.uniform(0, delay * 0.2)
                sleep = delay + jitter
                log.info("Sleeping %.2fs before retrying...", sleep)
                time.sleep(sleep)
        # If we exit loop, raise last exception
        raise last_exc
    return wrapper

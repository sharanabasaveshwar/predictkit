"""Exponential backoff retry utility."""
import time, logging, functools
logger = logging.getLogger(__name__)

def with_retry(max_attempts=5, base_delay=2, max_delay=60):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    if attempt == max_attempts:
                        raise
                    logger.warning("%s failed (attempt %d/%d): %s. Retrying in %ds…",
                                   fn.__name__, attempt, max_attempts, exc, delay)
                    time.sleep(delay)
                    delay = min(delay * 2, max_delay)
        return wrapper
    return decorator

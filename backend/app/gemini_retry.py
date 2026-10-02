"""Retry a Gemini call on the free tier's 429s, 5xx overload errors, and the
intermittent raw connection drops observed under load - all three were seen
in practice while building this, not hypothetical.
"""

import time
from typing import Callable, TypeVar

import httpx
from google.genai import errors

T = TypeVar("T")

RETRYABLE = (errors.ServerError, httpx.TransportError)


def with_retry(fn: Callable[[], T], retries: int = 6) -> T:
    delay = 5.0
    for attempt in range(retries):
        try:
            return fn()
        except errors.ClientError as e:
            if e.code == 429 and attempt < retries - 1:
                print(f"    rate limited, waiting {delay:.0f}s...")
                time.sleep(delay)
                delay *= 2
            else:
                raise
        except RETRYABLE as e:
            if attempt < retries - 1:
                print(f"    {type(e).__name__}, waiting {delay:.0f}s...")
                time.sleep(delay)
                delay *= 2
            else:
                raise

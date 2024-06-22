from datetime import datetime, timezone
from datetime import date

def make_naive(dt):
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt
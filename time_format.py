def is_valid_time(t: str) -> bool:
    try:
        h, m = t.split(':')
        h, m = int(h), int(m)
        return 0 <= h <= 23 and 0 <= m <= 59
    except ValueError:
        return False
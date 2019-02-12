str2strip=lambda s:s.strip() if s else s

def format_str(s, *args, **kwargs):
    if not s: return s
    return s.format(*args, **kwargs)
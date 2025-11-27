import re

def validate_password(p):
    if len(p) < 5:
        return False, "Password must be at least 5 characters."
    if not re.search(r'[A-Z]', p):
        return False, "Password must contain at least one capital letter."
    return True, ""

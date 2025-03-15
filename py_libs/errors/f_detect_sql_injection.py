def detect_sql_injection(user_input):
    """SQL injection detector"""
    sql_patterns = ["'", "--", ";", "/*", "*/", "xp_"]
    return any(pattern in user_input.lower() for pattern in sql_patterns)
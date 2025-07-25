# password_analyzer.py
from zxcvbn import zxcvbn

def analyze_password(password: str) -> dict:
    result = zxcvbn(password)
    return {
        "score": result["score"],
        "feedback": result["feedback"],
        "crack_times_display": result["crack_times_display"]
    }

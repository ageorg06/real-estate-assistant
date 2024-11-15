def validate_email(email: str) -> bool:
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[1]

def validate_phone(phone: str) -> bool:
    """Basic phone number validation"""
    digits = ''.join(filter(str.isdigit, phone))
    return len(digits) >= 10
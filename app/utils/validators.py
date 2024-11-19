def validate_email(email: str) -> bool:
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[1]

def validate_phone(phone: str) -> bool:
    """Validate Cyprus phone numbers
    Valid formats: 99XXXXXX, 96XXXXXX, 95XXXXXX, 97XXXXXX
    where X are digits and total length should be 8 digits
    """
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) != 8:
        return False
        
    valid_prefixes = ('99', '96', '95', '97')
    return digits.startswith(valid_prefixes)
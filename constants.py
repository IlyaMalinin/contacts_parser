EMAIL_PATTERNS = (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',)
PHONE_PATTERNS = (
    r'\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}',
    r'8\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}',
    r'\+7-\d{3}-\d{3}-\d{2}-\d{2}',
    r'\b\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}\b',
    r'\(\d{3}\)\s?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}',
)
LIMITATION_URL = 100

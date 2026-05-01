import re

def fix_spaced_text(text):
    text = re.sub(r'(\b\w(?:\s\w){2,})\b', lambda m: m.group(0).replace(" ", ""), text)
    text = re.sub(r'\s*\.\s*', '.', text)
    text = re.sub(r'\s*@\s*', '@', text)

    return text


import re





def extract_regex_phone_email(text):

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    phone_pattern = r"\+?[1-9]\d{6,14}"

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    return {
        "phone": phones,
        "email": emails
    }


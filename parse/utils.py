import encryption
import re

def fix_spaced_text(text):
    text = re.sub(r'(\b\w(?:\s\w){2,})\b', lambda m: m.group(0).replace(" ", ""), text)
    text = re.sub(r'\s*\.\s*', '.', text)
    text = re.sub(r'\s*@\s*', '@', text)

    return text


import re





def extract_regex_phone_email(text):

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    phone_pattern = r"(?:\+\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    return {
        "phone": phones,
        "email": emails
    }



#anonimize the personal infromation



from cryptography.fernet import Fernet
from django.conf import settings

fernet=Fernet(settings.PII_ENCRYPTION_KEY.encode())


def anonimize_personal_info(payload):
    def secure_encrypt(value):
        if value is None:
            value = ""
        elif isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        else:
            value = str(value)
        return fernet.encrypt(value.encode()).decode()

    return {
        "name": secure_encrypt(payload.get("name")),
        "email": secure_encrypt(payload.get("email")),
        "phone": secure_encrypt(payload.get("phone")),
        "address": secure_encrypt(payload.get("address"))
    }




    
    
    
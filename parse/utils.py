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
    phone_pattern = r"(?<![\w@])(?:\+?\d[\d().\-\s]{6,}\d)(?![\w@])"

    emails = re.findall(email_pattern, text)
    phone_matches = re.findall(phone_pattern, text)

    phones = []
    seen_digits = set()
    for phone in phone_matches:
        phone = phone.strip()
        digits = re.sub(r"\D", "", phone)
        if not 7 <= len(digits) <= 15:
            continue
        if any(digits in existing or existing in digits for existing in seen_digits):
            continue
        seen_digits.add(digits)
        phones.append(phone)

    return {
        "phone": phones,
        "email": emails
    }



#anonimize the personal infromation



from cryptography.fernet import Fernet
from django.conf import settings

fernet=Fernet(settings.PII_ENCRYPTION_KEY.encode())



def secure_encrypt(value):
        if value is None:
            value = ""
        elif isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        else:
            value = str(value)
        return fernet.encrypt(value.encode()).decode()

def anonimize_personal_info(payload):
  

    return {
        "name": secure_encrypt(payload.get("name")),
        "email": secure_encrypt(payload.get("email")),
        "phone": secure_encrypt(payload.get("phone")),
        "address": secure_encrypt(payload.get("address"))
    }

def decrypt_personal_info(encrypted_payload):
    def secure_decrypt(value):
        if not value:
            return ""
        if isinstance(value, list):
            return [secure_decrypt(v) for v in value]
        try:
            return fernet.decrypt(value.encode()).decode()
        except Exception:
            return "Decryption failed"

    return {
        "name": secure_decrypt(encrypted_payload.get("name")),
        "email": secure_decrypt(encrypted_payload.get("email")),
        "phone": secure_decrypt(encrypted_payload.get("phone")),
        "address": secure_decrypt(encrypted_payload.get("address"))
    }

import hashlib,hmac
from django.conf import settings



def generate_blind_index(value):
    if value is None:
        return None

    if isinstance(value, (list, tuple, set)):
        value = next((str(item).strip() for item in value if str(item).strip()), "")
    else:
        value = str(value).strip()

    if not value:
        return None

    idx=hmac.new(settings.BLIND_INDEX_KEY.encode(),
                 value.encode(),
                 digestmod=hashlib.sha256).hexdigest()
    return idx

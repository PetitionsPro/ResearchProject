import hashlib,hmac
from django.conf import settings



def generate_blind_index(value):
    idx=hmac.new(settings.BLIND_INDEX_KEY.encode(),
                 value.encode(),
                 digestmod=hashlib.sha256).hexdigest()
    return idx
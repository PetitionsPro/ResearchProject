

def mask_emails(email):
    if type(email)!=list:
        email=[email]
    masked_emails=[]
    for e in email:
        if '@' in e:
            local_part, domain = e.split('@')
            masked_local = local_part[0] + '****' + local_part[-1] if len(local_part) > 2 else local_part[0] + '****'
            masked_email = masked_local + '@' + domain
            masked_emails.append(masked_email)
        else:
            masked_emails.append(e)
    return masked_emails


def mask_phones(phone):
    if type(phone)!=list:
        phone=[phone]
    masked_phones=[]
    for p in phone:
        digits = ''.join(filter(str.isdigit, p))
        if len(digits) > 4:
            masked_phone = '****' + digits[-4:]
            masked_phones.append(masked_phone)
        else:
            masked_phones.append(p)
    return masked_phones



def mask_addresses(address):
    if type(address)!=list:
        address=[address]
    masked_addresses=[]
    for a in address:
        if len(a) > 10:
            masked_address = a[:5] + '****' + a[-5:]
            masked_addresses.append(masked_address)
        else:
            masked_addresses.append(a)
    return masked_addresses
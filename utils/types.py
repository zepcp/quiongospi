import settings

import re

def is_email(email):
    return re.fullmatch(r"[a-zA-Z0-9_.+-]{1,64}"
                        r"@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
                        email) is not None and len(email) <= settings.NAME

def is_wallet(wallet):
    return re.fullmatch(r"0x[0-9a-f]{40}", wallet.lower()) is not None

def email(value):
    if is_email(value):
        username, domain = value.split("@")
        return "@".join([username.lower(), domain.lower()])
    else:
        raise ValueError("Not an email address")

def wallet(value):
    if is_wallet(value):
        return value.lower()
    else:
        raise ValueError("Not a valid wallet address")


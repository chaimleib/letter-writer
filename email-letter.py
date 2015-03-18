import os
from os import path

from django.template import Template, Context
import settings as my_settings
from django.conf import settings

settings.configure(my_settings)

def load_addresses(names_path, delim=':'):
    with open(names_path, 'r') as f:
        lines = f.readlines()

    fields = [l.split(delim) for l in lines]
    addresses = []
    for f in fields:
        f = [s.strip() for s in f]

        to = [addr.strip() for addr in f[0].split(',')]
        cc = [addr.strip() for addr in f[1].split(',')] if len(f) > 1 else None
        bcc = [addr.strip() for addr in f[2].split(',')] if len(f) > 2 else None
        data = {
            'to': to,
            'cc': cc,
            'bcc': bcc,
        }
        addresses.append(data)

    return addresses

if __name__ == '__main__':
    print(settings.EMAIL_HOST_USER)
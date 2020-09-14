import base64
import os
import re

import requests

vault_regex = re.compile(r'vault:v\d+:[A-Za-z0-9+/=]+')
# vault:v1:mSZflft5ZX2gsI4U7r+04l1/BWCu9gTsm5Tz2enBIrsX6n9b/P2/Td+aNEGCaUzXvFOR9PSpuuLz1LKkFVRwsCn1HvhOYlcLhQ==

address = os.environ.get('VAULT_ADDR')
token = os.environ.get('VAULT_TOKEN')
key = 'cassiecluster'


def decrypt(ciphertext):
    resp = requests.request(
        'POST', f'{address}/v1/transit/decrypt/{key}',
        json={'ciphertext': ciphertext},
        headers={'X-Vault-Token': token},
    )
    resp.raise_for_status()
    return base64.decodebytes(resp.json()['data']['plaintext'].encode()).decode()


def encrypt(plaintext):
    resp = requests.request(
        'POST', f'{address}/v1/transit/encrypt/{key}',
        json={'plaintext': base64.encodebytes(plaintext.encode()).decode()},
        headers={'X-Vault-Token': token},
    )
    resp.raise_for_status()
    return resp.json()['data']['ciphertext']
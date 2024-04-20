from hashlib import sha384
from json import dumps, loads
from requests import request
from getpass import getpass
from ..JSON import JSON
from ...imconfig import CONFIG_PATH

config = JSON(CONFIG_PATH)

def checkWebhook(url: str):
    conditions = [
        lambda: url.startswith('https://discord.com/api/webhooks/') or url.startswith('https://discordapp.com/api/webhooks/'),
        lambda: request('GET', url).status_code == 200
    ]
    
    for condition in conditions:
        if not condition():
            return False
    
    return True

def getUserData():
    while not checkWebhook(webhook_url := input('Webhook URL > ')):
        print('Invalid Webhook')

    config.set('webhook/url', webhook_url)

    vault_passkey = getpass('Vault passkey > ')
    vault_passkey_hashed = sha384(vault_passkey.encode()).hexdigest()
    config.set('vault/passkey_hash', vault_passkey_hashed)


def genWebhookTable():
    pass

def init():
    getUserData()
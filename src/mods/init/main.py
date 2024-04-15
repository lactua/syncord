from hashlib import sha256
from json import dumps, loads
from requests import request
from getpass import getpass
from ..config import Config

config = Config()

def checkWebhook(url: str):
    conditions = [
        url.startswith('https://discord.com/api/webhooks/') or url.startswith('https://discordapp.com/api/webhooks/'),
        request('GET', url).status_code == 200
    ]

    return all(conditions)

def getUserData():
    while not checkWebhook(webhook_url := input('Webhook URL > ')):
        print('Invalid Webhook')
    config.set('webhook/url', webhook_url)

    vault_passkey = getpass('Vault passkey > ')
    vault_passkey_hashed = sha256(vault_passkey.encode()).hexdigest()
    config.set('vault/passkey_hash', vault_passkey_hashed)


def generateWebhookTable():
    pass

def init():
    getUserData()
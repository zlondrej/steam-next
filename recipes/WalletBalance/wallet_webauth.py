import re
from getpass import getpass

import steam.webauth as wa

username = input("Username: ")
password = getpass("Password: ")

webclient = wa.WebAuth(username, password)

try:
    webclient.login()
except wa.LoginIncorrect:
    webclient.login(password=input("Password: "))
except wa.TwoFactorAuthNotProvided:
    webclient.login(code=input("2FA code: "))

if webclient.logged_on:
    resp = webclient.session.get('https://store.steampowered.com/account/store_transactions/')
    resp.raise_for_status()
    balance = re.search(r'store_transactions/">(?P<balance>.*?)</a>', resp.text).group('balance')
    print("Current balance: %s" % balance)

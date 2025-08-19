import sys
try:
    import keyring
except Exception as e:
    print('Please install keyring: pip install keyring')
    raise

if len(sys.argv) < 3:
    print('Usage: python store_credentials.py <username> <password>')
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

keyring.set_password('auto_login', 'username', username)
keyring.set_password('auto_login', 'password', password)
print('Credentials stored to system keyring under service name "auto_login".')

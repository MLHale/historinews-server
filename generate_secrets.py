'''
This file should be ran as a user with root priveleges
'''
from django.utils.crypto import get_random_string
import os,sys,string

if len(sys.argv) > 1:
    SECRET_FILE = sys.argv[1]
else:
    SECRET_FILE = '/opt/historinews-server/historinews/secret.py'

_generated_code_template = '''
# Django secret key
SECRET_KEY = '{secret}'

# PostgreSQL information
DB_NAME = '{dbname}'
DB_USER = '{dbuser}'
DB_PASSWORD = '{dbpassword}'
DB_HOST = '{dbhost}'
DB_PORT = '{dbport}'
'''

_postgres_setup_template = '''(sudo -u postgres psql -c "CREATE USER {dbuser} WITH PASSWORD '{dbpassword}';") \\
  || (sudo -u postgres psql -c "ALTER USER {dbuser} WITH PASSWORD '{dbpassword}';"); \\
sudo -u postgres psql -c "CREATE DATABASE {dbname};"; \\
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {dbname} to {dbuser};";
'''

def main():
    secret_chars = ''.join(map(chr, range(128)))
    password_chars = string.ascii_letters + string.digits
    
    # generate new django secret
    secret = get_random_string(50, secret_chars)
    
    # set database information
    dbname = 'historinews'
    dbuser = 'historinews'
    dbpassword = get_random_string(50, password_chars)
    dbhost = 'localhost'
    dbport = ''

    # generate secret file
    generated_code = _generated_code_template.format(
        secret = secret.encode('base64').replace('\n',''),
        dbname = dbname,
        dbuser = dbuser,
        dbpassword = dbpassword,
        dbhost = dbhost,
        dbport = dbport,
    )
    
    postgres_setup = _postgres_setup_template.format(
        dbname = dbname,
        dbuser = dbuser,
        dbpassword = dbpassword,
    )
    os.system(postgres_setup)

    # save secret file
    with open(SECRET_FILE, 'wb') as f:
        f.write(generated_code)

    # modify access, since running as escalated user
    os.system('sudo chown $USER:www-data {secret_file} && sudo chmod 750 {secret_file}'.format(secret_file=SECRET_FILE))

if __name__ == '__main__':
    main()

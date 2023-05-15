import configparser
from cryptography.fernet import Fernet

# KEY FOR DECRYPT INFORMATIONS DB
fernet = Fernet(b'KEYDECRYPT')


# CLASS CONNECTION
class db_conn:
    ini = configparser.ConfigParser()
    ini.sections()
    ini.read("core/connection/config.ini")
    ini.sections()
    host = fernet.decrypt(ini['PRODUCAO']['host'].encode('utf-8')).decode('utf-8')
    user = fernet.decrypt(ini['PRODUCAO']['user'].encode('utf-8')).decode('utf-8')
    port = fernet.decrypt(ini['PRODUCAO']['port'].encode('utf-8')).decode('utf-8')
    password = fernet.decrypt(ini['PRODUCAO']['password'].encode('utf-8')).decode('utf-8')
    dbname = fernet.decrypt(ini['PRODUCAO']['dbname'].encode('utf-8')).decode('utf-8')
import hashlib

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import connection


class LegacyDatabaseBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        with connection.cursor() as cursor:
            username = username.upper()
            password = password.upper()
            cursor.execute(f"SELECT id, login, senha, nome FROM core_usuario WHERE 1 = 1 and login = '{username}'")
            row = cursor.fetchone()
            if row:
                if row[2] == hashlib.md5(password.encode()).hexdigest():
                    try:
                        user = User.objects.get_or_create(username=username)[0]
                    except:
                        user = User(username=username)
                        user.is_staff = False
                        user.is_superuser = False
                        user.save()
                    return user

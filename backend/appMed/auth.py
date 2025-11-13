from typing import Optional, Tuple
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .models import Registro


class RegistroUser:
    def __init__(self, registro: Registro):
        self.registro = registro
        self.is_authenticated = True

    @property
    def id(self):
        return self.registro.id

    def __str__(self):
        return f"RegistroUser<{self.registro.email}>"


class RegistroJWTAuthentication(BaseAuthentication):
    keyword = b"Bearer"

    def authenticate(self, request) -> Optional[Tuple[RegistroUser, str]]:
        auth = get_authorization_header(request).split()
        if not auth:
            return None
        if auth[0].lower() != self.keyword.lower():
            return None
        if len(auth) == 1:
            raise AuthenticationFailed("Token ausente.")
        if len(auth) > 2:
            raise AuthenticationFailed("Token inválido.")

        token = auth[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])  # type: ignore
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expirado.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Token inválido.")

        sub = payload.get("sub")
        if not sub:
            raise AuthenticationFailed("Token sem subject.")

        try:
            registro = Registro.objects.get(id=sub)
        except Registro.DoesNotExist:
            raise AuthenticationFailed("Usuário não encontrado.")

        return RegistroUser(registro), token.decode() if isinstance(token, bytes) else token  # type: ignore


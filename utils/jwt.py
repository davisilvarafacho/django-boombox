import jwt
import uuid

from django.conf import settings
from django.utils import timezone

from .env import get_environ_var

API_SECRET_KEY = get_environ_var('DJANGO_SECRET_KEY')
API_AUDIENCE = settings.SIMPLE_JWT["AUDIENCE"]
API_ISSUER = settings.SIMPLE_JWT["ISSUER"]
DEFAULT_JWT_PAYLOAD_CONTENT = {
    "token_type": "access",
    "exp": timezone.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
    "iat": timezone.now(),
    "jti": uuid.uuid4().hex,
    "aud": API_AUDIENCE,
    "iss": API_ISSUER,
}


def decode_jwt(token: str):
    payload = jwt.decode(token, key=API_SECRET_KEY, audience=API_AUDIENCE)
    return payload


def generate_jwt(token_type: str, payload: dict):
    payload = {"type": token_type, **DEFAULT_JWT_PAYLOAD_CONTENT, **payload}
    token = jwt.encode(payload=payload, algorithm='HS256', key=API_SECRET_KEY)
    return token

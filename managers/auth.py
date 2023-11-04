from typing import Optional

import jwt
from datetime import datetime, timedelta
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from db import database
from models import user, RoleType


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                'sub': user['id'],
                'exp': datetime.utcnow() + timedelta(minutes=120)
            }
            return jwt.encode(payload, config('SECRET_KEY'), algorithm='HS256')
        except Exception as ex:
            # Log the exception
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, config('SECRET_KEY'), algorithms=['HS256'])
            user_data = await database.fetch_one(user.select().where(user.c.id == payload['sub']))
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, 'Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(401, 'Token is invalid')


oauth2_scheme = CustomHTTPBearer()


def is_complainer(request: Request):
    if not request.state.user['role'] == RoleType.complainer:
        raise HTTPException(403, 'Forbidden: you are not complainer')


def is_approver(request: Request):
    if not request.state.user['role'] == RoleType.approver:
        raise HTTPException(403, 'Forbidden: you are not approver')


def is_admin(request: Request):
    if not request.state.user['role'] == RoleType.admin:
        raise HTTPException(403, 'Forbidden: you are not admin')

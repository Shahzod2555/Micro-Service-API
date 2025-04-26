from datetime import datetime, timedelta

from fastapi import HTTPException
import jwt

from src.api.schemas import AuthUserRead, TokenResponse
from src.config import settings


async def create_jwt(user_data: AuthUserRead, expr: int):
    expire = datetime.now() + timedelta(minutes=expr)
    user_data_dict = user_data.model_dump()
    user_data_dict["exp"] = expire.timestamp()
    jwt_token = jwt.encode(
        payload=user_data_dict, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return jwt_token


async def create_access_token(data: AuthUserRead) -> str:
    return await create_jwt(data, settings.ACCESS_EXPIRE)


async def create_refresh_token(data: AuthUserRead) -> str:
    return await create_jwt(data, settings.REFRESH_EXPIRE)


async def create_token(data: AuthUserRead) -> TokenResponse:
    access = await create_access_token(data)
    refresh = await create_refresh_token(data)
    return TokenResponse(access=access, refresh=refresh)


async def decode_jwt(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен просрочен")

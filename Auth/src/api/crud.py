from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.hash_password import verify_password, hash_password
from src.api.jwt import create_token
from src.core.models import AuthUser
from src.api.schemas import UserCreate, AuthUserRead, UserLogin, TokenResponse


async def create_user(session: AsyncSession, user_data: UserCreate) -> TokenResponse:
    for field in ("email", "username", "phone"):
        existing_user = await get_user_by_field(
            session, field, getattr(user_data, field)
        )
        if existing_user is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    user = AuthUser(**user_data.model_dump())
    user.password = hash_password(user.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return await create_token(AuthUserRead.model_validate(user))


async def get_user_by_field(
    session: AsyncSession, field_name: str, field_value: str
) -> AuthUser | None:
    if not hasattr(AuthUser, field_name):
        raise ValueError(f"Field {field_name} does not exist")
    stmt = select(AuthUser).where(getattr(AuthUser, field_name) == field_value)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def login(
    session: AsyncSession, field_name: str, field_value: str, user_data: UserLogin
) -> TokenResponse:
    user = await get_user_by_field(session, field_name, field_value)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return await create_token(AuthUserRead.model_validate(user))

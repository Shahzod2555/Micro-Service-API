from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from src.core.db import db_helper
from src.api.schemas import UserLogin, TokenResponse, UserCreate
from src.api import crud

router = APIRouter()


@router.post('/register', response_model=TokenResponse)
async def register(
        register_data: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.create_user(session, register_data)


@router.post("/login/{field_name}", response_model=TokenResponse)
async def login(
    field_name: str,
    login_data: UserLogin,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if field_name not in ("email", "username", "phone"):
        raise HTTPException(status_code=400, detail="Invalid login field")
    field_value = getattr(login_data, field_name)
    return await crud.login(session, field_name, field_value, login_data)

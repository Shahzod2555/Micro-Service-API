from pydantic import BaseModel, EmailStr, ConfigDict, model_validator


class UserLogin(BaseModel):
    username: str | None = None
    password: str
    email: EmailStr | None = None
    phone: str | None = None


class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: str
    first_name: str

class UserCreate(UserBase):
    password: str

class TokenResponse(BaseModel):
    access: str
    refresh: str


class AuthUserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

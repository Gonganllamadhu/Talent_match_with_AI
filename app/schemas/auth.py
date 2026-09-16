from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email : EmailStr
    name : str = Field(
        min_length=5,
        max_length=200
    )
    password: str = Field(
        min_length=8,
        max_length=128
    )

    phone: str | None = Field(
        default=None,
        max_length=20
    )

    role_id: int | None = None

    department_id: int | None = None


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "bearer"


class UserResponse(BaseModel):

    id: int
    email: EmailStr
    name: str | None
    phone: str | None
    role_id: int
    department_id: int | None
    is_active: bool

    model_config = {
        "from_attributes": True
    }


class SignupResponse(BaseModel):

    user: UserResponse
    tokens: TokenResponse

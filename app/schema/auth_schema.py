from pydantic import BaseModel


from pydantic import Field


class UserLogin(BaseModel):
    username: str = Field(..., example="user123")
    password: str = Field(..., example="strongpassword")


class LoginResponse(BaseModel):
    access_token: str
    token_type: str

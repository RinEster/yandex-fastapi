from pydantic import BaseModel, SecretStr, Field, EmailStr


class User(BaseModel):
    id: int
    login: str = Field(..., max_length=50)
    email: EmailStr
    password: SecretStr
    first_name: str | None = Field(None,max_length=50)
    second_name: str | None = Field(None,max_length=50)
    

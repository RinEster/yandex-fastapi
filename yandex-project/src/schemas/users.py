from pydantic import BaseModel, Field, EmailStr, SecretStr, ConfigDict, field_validator

class User(BaseModel):
    login: str = Field(..., max_length=50)
    email: EmailStr
    first_name: str | None = Field(None, max_length=50)
    second_name: str | None = Field(None, max_length=50)
    model_config = ConfigDict(from_attributes=True)

class UserCreate(User):
    password: SecretStr = Field(..., min_length=8, max_length=128)
    
    @field_validator("password", mode="after")
    @staticmethod
    def check_password(password: SecretStr) -> SecretStr:
        if len(password) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")

        return password


class UserResponse(User):
    id: int
    model_config = ConfigDict(from_attributes=True)


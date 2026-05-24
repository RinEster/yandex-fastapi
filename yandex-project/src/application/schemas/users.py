from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
)


class UserBase(BaseModel):
    login: str = Field(..., max_length=50)
    email: EmailStr
    first_name: str | None = Field(
        None, max_length=50, description="Имя"
    )
    second_name: str | None = Field(
        None, max_length=50, description="Фамилия"
    )


class UserCreate(UserBase):
    password: SecretStr = Field(
        ..., min_length=8, max_length=128
    )

    @field_validator("password")
    @classmethod
    def validate_password_complexity(
        cls, value: SecretStr
    ) -> SecretStr:
        raw_password = value.get_secret_value()

        if not any(char.isdigit() for char in raw_password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну цифру"
            )
        if not any(char.isupper() for char in raw_password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну заглавную букву"
            )

        return value


class UserUpdate(BaseModel):
    login: str | None = Field(None, max_length=50)
    email: EmailStr | None = None
    first_name: str | None = Field(
        None, max_length=50, description="Имя"
    )
    second_name: str | None = Field(
        None, max_length=50, description="Фамилия"
    )

    password: SecretStr | None = Field(
        None, min_length=8, max_length=128
    )

    @field_validator("password")
    @classmethod
    def validate_password_complexity(
        cls, value: SecretStr | None
    ) -> SecretStr | None:
        if value is None:
            return value

        raw_password = value.get_secret_value()

        if not any(char.isdigit() for char in raw_password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну цифру"
            )

        if not any(char.isupper() for char in raw_password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну заглавную букву"
            )

        return value


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

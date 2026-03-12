from pydantic.types import SecretStr
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema

class GetUserByEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, email: str) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.get_user_by_email(session, email)
            
            if not user:
                raise ValueError("Пользователь не найден")
            
            user_dict = {
                "id": user.id,
                "login": user.login,
                "email": user.email,
                "password": SecretStr(user.password),
                "first_name": user.first_name,
                "second_name": user.second_name
            }
            
            return UserSchema.model_validate(obj=user_dict)

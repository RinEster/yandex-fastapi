from pydantic import SecretStr
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema

class UpdateUserPasswordUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, new_password: str) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.get_user_by_id(session, user_id)
            if not user:
                raise ValueError("Пользователь не найден")
            
            updated = self._repo.update_password(session, user_id, new_password)
            
            user_dict = {
                "id": updated.id,
                "login": updated.login,
                "email": updated.email,
                "password": SecretStr(updated.password),
                "first_name": updated.first_name,
                "second_name": updated.second_name
            }

            return UserSchema.model_validate(obj=user_dict)

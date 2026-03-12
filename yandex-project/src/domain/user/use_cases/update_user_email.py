from pydantic import SecretStr
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema

class UpdateUserEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    def validate_email(self, email: str) -> None:
        if '@' not in email:
            raise ValueError("Email должен содержать символ '@'")



    async def execute(self, user_id: int, new_email: str) -> UserSchema:
        with self._database.session() as session:
            try:
                self.validate_email(new_email)
                user = self._repo.get_user_by_id(session, user_id)
                if not user:
                    raise ValueError("Пользователь не найден")
            
                exist_email = self._repo.get_user_by_email(session, new_email)
                if exist_email and exist_email.id != user_id:
                    raise ValueError("Пользователь с данным email уже существует")
            
                updated = self._repo.update_email(session, user_id, new_email)
           
                user_dict = {
                    "id": updated.id,
                    "login": updated.login,
                    "email": updated.email,
                    "password": SecretStr(updated.password),
                    "first_name": updated.first_name,
                    "second_name": updated.second_name
                }

                return UserSchema.model_validate(obj=user_dict)
            except ValueError as e:
                session.rollback()
                raise e


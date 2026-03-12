from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema

class UpdateUserEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, new_email: str) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.get_user_by_id(session, user_id)
            if not user:
                raise ValueError("Пользователь не найден")
            
            exist_email = self._repo.get_user_by_email(session, new_email)
            if exist_email and exist_email.id != user_id:
                raise ValueError("Пользователь с данным email уже существует")
            
            updated = self._repo.update_email(session, user_id, new_email)
            
            return UserSchema.model_validate(obj=updated)

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema

class UpdateUserLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, new_login: str) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.get_user_by_id(session, user_id)
            if not user:
                raise ValueError("Пользователь не найден")
            
            exist_login = self._repo.get_user_by_login(session, new_login)
            if exist_login and exist_login.id != user_id:
                raise ValueError("Пользователь с данным логином уже существует")
            
            updated = self._repo.update_login(session, user_id, new_login)
            
            return UserSchema.model_validate(obj=updated)

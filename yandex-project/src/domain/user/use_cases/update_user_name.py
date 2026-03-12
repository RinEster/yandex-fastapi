from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema

class UpdateUserNameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, new_first_name: str, new_second_name: str) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.get_user_by_id(session, user_id)
            if not user:
                raise ValueError("Пользователь не найден")
            
            updated = self._repo.update_name(session, user_id, new_first_name, new_second_name)
            
            return UserSchema.model_validate(obj=updated)

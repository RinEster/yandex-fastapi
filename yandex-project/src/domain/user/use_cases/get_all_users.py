from typing import List

from pydantic import SecretStr
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema

class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> List[UserSchema]:
        with self._database.session() as session:
            users = self._repo.get_all_user(session)
            
            result = []
            for user in users:
                user_dict = {
                    "id": user.id,
                    "login": user.login,
                    "email": user.email,
                    "password": SecretStr(user.password), 
                    "first_name": user.first_name,
                    "second_name": user.second_name
                }
                result.append(UserSchema.model_validate(obj=user_dict))
            
            return result

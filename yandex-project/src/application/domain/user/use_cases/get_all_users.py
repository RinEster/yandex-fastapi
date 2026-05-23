from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserResponse


class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> List[UserResponse]:
        with self._database.session() as session:
            users = self._repo.get_all_user(session)
            return [UserResponse.model_validate(user) for user in users]

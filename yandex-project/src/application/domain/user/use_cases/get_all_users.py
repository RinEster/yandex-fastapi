from typing import List
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserResponse


class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> List[UserResponse]:
        async with self._database.session() as session:
            users = await self._repo.get_all_user(session=session)
            return [UserResponse.model_validate(obj=u) for u in users]

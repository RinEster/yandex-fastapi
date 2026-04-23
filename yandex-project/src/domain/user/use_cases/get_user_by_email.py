from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserResponse


class GetUserByEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, email: str) -> UserResponse:
        with self._database.session() as session:
            user = self._repo.get_user_by_email(session, email)
            return UserResponse.model_validate(user)

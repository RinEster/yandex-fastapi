from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserCreate, UserResponse


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserResponse:
        with self._database.session() as session:
            user = self._repo.create(session=session, data=data)
            return UserResponse.model_validate(user)

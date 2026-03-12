from pydantic import SecretStr
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema

class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()


    def validate_email(self, email: str) -> None:
        if '@' not in email:
            raise ValueError("Email должен содержать символ '@'")

    async def execute(
        self, 
        login: str, 
        email: str, 
        password: str,
        first_name: str | None = None,
        second_name: str | None = None
    ) -> UserSchema:
        with self._database.session() as session:
            try:
                self.validate_email(email)
                exist_login=self._repo.get_user_by_login(session, login)
                if exist_login:
                    raise ValueError("Пользователь с таким логином уже существует")

                exist_email=self._repo.get_user_by_email(session, email)
                if exist_email:
                    raise ValueError("Пользователь с такой почтой уже существует")
           

                user = self._repo.create(
                    session=session,
                    login=login,
                    email=email,
                    password=password,
                    first_name=first_name,
                    second_name=second_name
                )

            
                user_data = {
                    "id":user.id,
                    "login":user.login,
                    "email":user.email,
                    "password":SecretStr(user.password),
                    "first_name":user.first_name,
                    "second_name":user.second_name
                }
            

                return UserSchema.model_validate(obj=user_data)
            except ValueError as e:
                session.rollback()
                raise e

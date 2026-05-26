from pydantic import EmailStr

class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с id = {id} не найдена"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundBySlugException(BaseDomainException):
    _exception_text_template = "Категория со slug = '{slug}' не найдена"

    def __init__(self, slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(slug=slug)

        super().__init__(detail=self._exception_text_template)


class CategorySlugIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Категория со slug = '{slug}' уже существует"

    def __init__(self, slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(slug=slug)

        super().__init__(detail=self._exception_text_template)

class CategoryTitleIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Категория с названием = '{title}' уже существует"
    
    def __init__(self, title: str) -> None:
        self._exception_text_template = self._exception_text_template.format(title=title)

        super().__init__(detail=self._exception_text_template)


class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Локация с id = '{id}' не найдена"
    
    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)
    
class WrongPasswordException(BaseDomainException):
    _exception_text = "Неверный пароль"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)



class UserNotFoundByLoginException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' не найден"

    def __init__(self, login: str) -> None:
        self._exception_text_template = self._exception_text_template.format(login=login)

        super().__init__(detail=self._exception_text_template)


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пользователь с id = {id} не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)

class UserNotFoundByEmailException(BaseDomainException):
    _exception_text_template = "Пользователь с почтой '{email}' не найден"

    def __init__(self, email: EmailStr) -> None:
        self._exception_text_template = self._exception_text_template.format(email=email)

        super().__init__(detail=self._exception_text_template)


class UserLoginIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с логином '{login}' уже существует"

    def __init__(self, login: str) -> None:
        self._exception_text_template = self._exception_text_template.format(login=login)

        super().__init__(detail=self._exception_text_template)



class UserEmailIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с почтой '{email}' уже существует"

    def __init__(self, email: EmailStr) -> None:
        self._exception_text_template = self._exception_text_template.format(email=email)

        super().__init__(detail=self._exception_text_template)

class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пост с id = {id} не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)

class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с id = {id} не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)

class LocationNameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Локация с именем = '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(name=name)

        super().__init__(detail=self._exception_text_template)

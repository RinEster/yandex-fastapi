class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail

class UserNotFoundException(BaseDatabaseException):
    pass


class UserLoginAlreadyExistsException(BaseDatabaseException):
    def __init__(self, login: str):
        self.login = login
        super().__init__(f"Login {login} already exists")


class UserEmailAlreadyExistsException(BaseDatabaseException):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email {email} already exists")


class PostNotFoundException(BaseDatabaseException):
    pass


class CategoryNotFoundException(BaseDatabaseException):
    pass


class CategorySlugAlreadyExistsException(BaseDatabaseException):
    pass

class CategoryTitleAlreadyExistsException(BaseDatabaseException):
    pass

class LocationNotFoundException(BaseDatabaseException):
    pass


class LocationNameAlreadyExistsException(BaseDatabaseException):
    pass


class CommentNotFoundException(BaseDatabaseException):
    pass


class CommentDoesNotHaveImageException(BaseDatabaseException):
    pass

class NotCommentAuthor(BaseDatabaseException):
    pass

class CommentImageNotFoundException(BaseDatabaseException):
    pass

class PostImageNotFoundException(BaseDatabaseException):
    pass

class NotPostAuthorException(BaseDatabaseException):
    pass

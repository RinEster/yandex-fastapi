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

class LocationTitleIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Локация с названием = '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(name=name)

        super().__init__(detail=self._exception_text_template)

class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Локация с id = '{id}' уже существует"
    
    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)
    


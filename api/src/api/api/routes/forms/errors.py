class ServiceError(Exception):
    """Base class for service exceptions."""

    pass


class GraphQLError(ServiceError):
    """Raised when GraphQL returns an error."""

    pass


class FormNotFoundError(ServiceError):
    """Raised when a form is not found."""

    def __init__(self, form: str) -> None:
        self._form = form
        super().__init__(f"Form {form} not found.")

    @property
    def form(self) -> str:
        return self._form


class FieldNotFoundError(ServiceError):
    """Raised when a form field is not found."""

    def __init__(self, field: str) -> None:
        self._field = field
        super().__init__(f"Field {field} not found.")

    @property
    def field(self) -> str:
        return self._field

class GraphQLError(Exception):
    """Base class for GraphQL exceptions."""

    def __init__(self, message: str | None = None) -> None:
        self._message = message

        args = (message,) if message else ()
        super().__init__(*args)

    @property
    def message(self) -> str | None:
        return self._message


class UnkownError(GraphQLError):
    """Raised when an unknown error occurs on the GraphQL service."""

    pass


class ConnectError(GraphQLError):
    """Raised when a connection error occurs on the GraphQL service."""

    pass


class InternalServerError(GraphQLError):
    """Raised when an internal server error occurs on the GraphQL service."""

    pass


class ForbiddenError(GraphQLError):
    """Raised when the user is not authorized to access the GraphQL service."""

    pass


class NotFoundError(GraphQLError):
    """Raised when the requested resource was not found on the GraphQL service."""

    pass

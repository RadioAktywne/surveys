from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_422_UNPROCESSABLE_ENTITY


class UnprocessableEntityException(HTTPException):
    """Unprocessable entity."""

    status_code = HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Unprocessable entity"

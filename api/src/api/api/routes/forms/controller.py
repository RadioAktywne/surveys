from typing import Annotated

from litestar import Controller as BaseController
from litestar import Response, get, post
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.params import Parameter

from api.api.exceptions import UnprocessableEntityException
from api.api.routes.forms.errors import FieldNotFoundError, FormNotFoundError
from api.api.routes.forms.models import (
    GetResponse,
    ListResponse,
    SubmitRequest,
    SubmitResponse,
)
from api.api.routes.forms.service import Service
from api.state import State


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(self, state: State) -> Service:
        return Service(
            graphql=state.graphql,
        )

    def build(self) -> dict[str, Provide]:
        return {
            "service": Provide(self._build_service),
        }


class Controller(BaseController):
    """Controller for the root endpoint."""

    dependencies = DependenciesBuilder().build()

    @get(
        summary="List all",
        description="List all forms with pagination",
    )
    async def list(
        self,
        service: Service,
        limit: Annotated[
            int | None,
            Parameter(
                title="Limit",
                description="The maximum number of forms to return.",
            ),
        ] = None,
        start: Annotated[
            int | None,
            Parameter(
                title="Start",
                description="The index of the first form to return.",
            ),
        ] = None,
    ) -> Response[ListResponse]:
        pager = await service.list(limit=limit, start=start)
        content = ListResponse(pager=pager)
        return Response(content)

    @get(
        "/{id:str}",
        summary="Get form",
        description="Get form by ID",
        raises=[NotFoundException],
    )
    async def get(
        self,
        id: Annotated[
            str,
            Parameter(
                title="ID",
                description="The ID of the form",
            ),
        ],
        service: Service,
    ) -> Response[GetResponse]:
        try:
            form = await service.get(id=id)
        except FormNotFoundError as e:
            raise NotFoundException(extra={"form": id}) from e

        content = GetResponse(form=form)
        return Response(content)

    @post(
        "/{id:str}/submit",
        summary="Submit form",
        description="Submit a form",
        raises=[NotFoundException, UnprocessableEntityException],
    )
    async def submit(
        self,
        id: Annotated[
            str,
            Parameter(
                title="ID",
                description="The ID of the form",
            ),
        ],
        service: Service,
        data: SubmitRequest,
    ) -> Response[SubmitResponse]:
        try:
            confirmation = await service.submit(id=id, submission=data.submission)
        except FormNotFoundError as e:
            raise NotFoundException(extra={"form": id}) from e
        except FieldNotFoundError as e:
            raise UnprocessableEntityException(extra={"field": e.field}) from e

        content = SubmitResponse(confirmation=confirmation)
        return Response(content)

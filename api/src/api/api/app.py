from contextlib import AbstractAsyncContextManager, asynccontextmanager
from importlib import metadata
from typing import AsyncGenerator, Callable

from litestar import Litestar, Router
from litestar.contrib.pydantic import PydanticPlugin
from litestar.openapi import OpenAPIConfig
from litestar.plugins import PluginProtocol

from api.api.routes.router import router
from api.config.models import Config
from api.graphql.client import GraphQLClient
from api.graphql.models import LoginRequest
from api.state import State


class AppBuilder:
    """Builds the app.

    Args:
        config: Config object.
    """

    def __init__(self, config: Config) -> None:
        self._config = config

    def _get_route_handlers(self) -> list[Router]:
        return [router]

    def _build_openapi_config(self) -> OpenAPIConfig:
        return OpenAPIConfig(
            title="api",
            version=metadata.version("api"),
            description="surveys api",
        )

    def _build_pydantic_plugin(self) -> PydanticPlugin:
        return PydanticPlugin(
            prefer_alias=True,
        )

    def _build_plugins(self) -> list[PluginProtocol]:
        return [
            self._build_pydantic_plugin(),
        ]

    def _build_graphql_client(self) -> GraphQLClient:
        return GraphQLClient(
            url=f"http://{self._config.graphql.host}:{self._config.graphql.port}/graphql",
            login=LoginRequest(
                username=self._config.graphql.user,
                password=self._config.graphql.password,
            ),
        )

    def _build_initial_state(self) -> State:
        return State(
            {
                "config": self._config,
                "graphql": self._build_graphql_client(),
            }
        )

    @asynccontextmanager
    async def _graphql_lifespan(self, app: Litestar) -> AsyncGenerator[None, None]:
        state: State = app.state

        async with state.graphql:
            yield

    def _build_lifespan(
        self,
    ) -> list[Callable[[Litestar], AbstractAsyncContextManager]]:
        return [
            self._graphql_lifespan,
        ]

    def build(self) -> Litestar:
        return Litestar(
            route_handlers=self._get_route_handlers(),
            openapi_config=self._build_openapi_config(),
            plugins=self._build_plugins(),
            state=self._build_initial_state(),
            lifespan=self._build_lifespan(),
        )

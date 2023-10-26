from pydantic import BaseModel, Field

from api.config.base import BaseConfig


class ServerConfig(BaseModel):
    """Configuration for the server."""

    host: str = Field(
        "0.0.0.0",
        title="Host",
        description="Host to run the server on.",
    )
    port: int = Field(
        30005,
        ge=0,
        le=65535,
        title="Port",
        description="Port to run the server on.",
    )


class GraphQLConfig(BaseModel):
    """Configuration for the GraphQL service."""

    host: str = Field(
        "localhost",
        title="Host",
        description="Host of the GraphQL service.",
    )
    port: int = Field(
        30004,
        ge=0,
        le=65535,
        title="Port",
        description="Port of the GraphQL service.",
    )
    user: str = Field(
        "admin",
        title="User",
        description="Username to use for the GraphQL service.",
    )
    password: str = Field(
        "password",
        title="Password",
        description="Password to use for the GraphQL service.",
    )


class Config(BaseConfig):
    """Configuration for the application."""

    server: ServerConfig = Field(
        ServerConfig(),
        title="Server",
        description="Configuration for the server.",
    )
    graphql: GraphQLConfig = Field(
        GraphQLConfig(),
        title="GraphQL",
        description="Configuration for the GraphQL service.",
    )

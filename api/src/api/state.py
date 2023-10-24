from litestar.datastructures import State as LitestarState

from api.config.models import Config
from api.graphql.client import GraphQLClient


class State(LitestarState):
    """Use this class as a type hint for the state of your application.

    Attributes:
        config: The configuration for the application.
    """

    config: Config
    graphql: GraphQLClient

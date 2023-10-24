from litestar import Router

from api.api.routes.forms.controller import Controller

router = Router(
    path="/forms",
    route_handlers=[
        Controller,
    ],
)

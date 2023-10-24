from litestar import Router

from api.api.routes.forms.router import router as forms_router

router = Router(
    path="/",
    route_handlers=[
        forms_router,
    ],
)

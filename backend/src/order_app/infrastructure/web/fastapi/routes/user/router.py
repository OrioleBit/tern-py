from fastapi import APIRouter
from starlette import status

from order_app.infrastructure.web.fastapi.routes.user.login import (
    LoginUserResponse,
    login_user,
)
from order_app.infrastructure.web.fastapi.routes.user.register import (
    RegisterUserResponse,
    register_user,
)

router = APIRouter()

router.add_api_route(
    "/register",
    methods=["POST"],
    endpoint=register_user,
    response_model=RegisterUserResponse,
    status_code=status.HTTP_201_CREATED,
)

router.add_api_route(
    "/login",
    methods=["POST"],
    endpoint=login_user,
    response_model=LoginUserResponse,
    status_code=status.HTTP_200_OK,
)

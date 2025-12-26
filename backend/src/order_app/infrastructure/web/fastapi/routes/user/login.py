from fastapi import Depends, HTTPException
from pydantic import BaseModel, EmailStr
from starlette import status

from order_app.infrastructure.composition_root import CompositionRoot
from order_app.infrastructure.web.fastapi.dependencies import get_composition_root
from order_app.interface.controllers.user.login_user import LoginUserInputDto


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str


class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int


def login_user(
    request: LoginUserRequest,
    composition_root: CompositionRoot = Depends(get_composition_root),
) -> LoginUserResponse:
    operation_result = composition_root.login_controller.handle(
        LoginUserInputDto(
            email=request.email,
            password=request.password,
        )
    )
    if operation_result.is_success:
        return LoginUserResponse(
            access_token=operation_result.success.access_token,
            token_type=operation_result.success.token_type,
            expires_in=operation_result.success.expires_in,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=operation_result.error.message,
        )

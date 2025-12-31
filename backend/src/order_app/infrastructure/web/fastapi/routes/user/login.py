from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from order_app.infrastructure.composition_root import CompositionRoot
from order_app.infrastructure.web.fastapi.dependencies import get_composition_root
from order_app.interface.controllers.user.login_user import LoginUserInputDto
from pydantic import BaseModel, EmailStr, constr
from starlette import status


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class LoginUserResponse(BaseModel):
    access_token: str
    refresh_token: str


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
        response = JSONResponse(
            content=LoginUserResponse(
                access_token=operation_result.success.access_token,
                refresh_token=operation_result.success.refresh_token,
            ).model_dump(),
        )
        response.set_cookie(
            key="access_token",
            value=operation_result.success.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=operation_result.success.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=operation_result.error.message,
        )

from uuid import UUID

from fastapi import Depends, HTTPException
from pydantic import BaseModel, EmailStr
from starlette import status

from order_app.infrastructure.composition_root import CompositionRoot
from order_app.infrastructure.web.fastapi.dependencies import get_composition_root
from order_app.interface.controllers.user.register_user import RegisterUserInputDto


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class RegisterUserResponse(BaseModel):
    user_id: UUID


def register_user(
    request: RegisterUserRequest,
    composition_root: CompositionRoot = Depends(get_composition_root),
):
    operation_result = composition_root.register_controller.handle(
        RegisterUserInputDto(
            name=request.name, email=request.email, password=request.password
        )
    )
    if operation_result.is_success:
        return RegisterUserResponse(user_id=operation_result.success.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=operation_result.error.message,
        )

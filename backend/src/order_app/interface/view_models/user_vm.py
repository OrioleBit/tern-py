from dataclasses import dataclass, field
from typing import Literal
from uuid import UUID


@dataclass
class UserViewModel:
    id: UUID
    name: str
    email: str
    role: str


@dataclass
class TokensViewModel:
    access_token: str
    # refresh_token: str


@dataclass
class RegisterUserViewModel:
    user: UserViewModel
    tokens: TokensViewModel


@dataclass
class LoginUserViewModel:
    user: UserViewModel
    access_token: str
    expires_in: int
    token_type: Literal["Bearer"] = field(default="Bearer")

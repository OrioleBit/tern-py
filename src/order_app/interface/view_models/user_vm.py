from dataclasses import dataclass, field
from typing import Literal


@dataclass
class UserViewModel:
    id: str
    name: str
    email: str
    role: str


@dataclass
class LoginUserViewModel:
    user: UserViewModel
    token: str
    expires_in: int
    token_type: Literal["Bearer"] = field(default="Bearer")

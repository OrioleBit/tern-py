from dataclasses import dataclass


@dataclass(frozen=True)
class OrderViewModel:
    id: str
    user_id: str
    items: list[dict]
    created_at: str
    updated_at: str | None
    total_price: str

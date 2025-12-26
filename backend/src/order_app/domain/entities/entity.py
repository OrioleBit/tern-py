from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4


@dataclass
class Entity:
    id: UUID

    @classmethod
    def new(cls, **kwargs) -> Self:
        """Create a new entity with a generated UUID."""
        return cls(id=uuid4(), **kwargs)

    @classmethod
    def from_existing(cls, id: UUID, **kwargs) -> Self:
        """Rehydrate an existing entity with a given UUID."""
        return cls(id=id, **kwargs)

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

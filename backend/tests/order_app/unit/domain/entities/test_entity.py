from uuid import UUID, uuid4

import pytest

from order_app.domain.entities.entity import Entity


class ConcreteEntity(Entity):
    pass


def test_new_entity_has_unique_id():
    e1 = ConcreteEntity.new()
    e2 = ConcreteEntity.new()

    assert e1.id is not None
    assert e2.id is not None
    assert isinstance(e1.id, UUID)
    assert isinstance(e2.id, UUID)
    assert e1.id != e2.id


def test_equality_not_implemented_other():
    e1 = ConcreteEntity.new()
    e2 = object()

    with pytest.raises(NotImplementedError):
        e1 != e2


def test_equality_based_on_id():
    test_id_1 = uuid4()
    test_id_2 = uuid4()
    e1 = ConcreteEntity.new()
    e1.id = test_id_1
    e2 = ConcreteEntity.new()
    e2.id = test_id_1
    e3 = ConcreteEntity.new()
    e3.id = test_id_2

    assert e1 == e2
    assert e1 != e3


def test_hashing():
    test_id = uuid4()
    e1 = ConcreteEntity.new()
    e1.id = test_id
    e2 = ConcreteEntity.new()
    e2.id = test_id

    entity_set = {e1}
    assert e2 in entity_set


def test_from_existing():
    test_id = uuid4()
    e1 = ConcreteEntity.from_existing(test_id)
    assert e1.id == test_id

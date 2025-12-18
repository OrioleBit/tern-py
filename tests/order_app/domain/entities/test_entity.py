from uuid import UUID, uuid4

from order_app.domain.entities.entity import Entity


class ConcreteEntity(Entity):
    pass


def test_new_entity_has_unique_id():
    e1 = ConcreteEntity.new()
    e2 = ConcreteEntity.new()
    assert e1.id is not None
    assert isinstance(e1.id, UUID)
    assert e1.id != e2.id


def test_equality_based_on_id():
    test_id = uuid4()
    e1 = ConcreteEntity.new()
    e1.id = test_id
    e2 = ConcreteEntity.new()
    e2.id = test_id
    e3 = ConcreteEntity.new()
    e3.id = uuid4()

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

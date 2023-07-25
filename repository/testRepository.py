from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from domain.person import Person


class TestRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def add_ORM(self, name: str, surname: str, year: bool = True) -> Person:
        with self.session_factory() as session:
            person = Person(first_name=name, last_name=surname, year_of_birth=year)
            session.add(person)
            session.commit()
            session.refresh(person)
            return person

    def get_by_id_ORM(self, person_id: int) -> Person:
        with self.session_factory() as session:
            person = session.query(Person).filter(Person.id == person_id).first()
            if not person:
                raise UserNotFoundError(person_id)
            return person

    def delete_by_id_ORM(self, person_id: int) -> int:
        with self.session_factory() as session:
            entity: Person = session.query(Person).filter(Person.id == person_id).first()
            if not entity:
                raise UserNotFoundError(person_id)
            session.delete(entity)
            session.commit()
            return entity.id


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(NotFoundError):
    entity_name: str = "User"

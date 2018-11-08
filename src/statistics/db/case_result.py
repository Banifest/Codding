from uuid import UUID

from src.statistics.db.entity import Entity


class CaseResult(Entity):
    guid: UUID
    quantity_correct_bit: int
    quantity_incorrect_bit: int
    quantity_repair_bit: int
    quantity_changed_bit: int

    def create(self):
        self._connection.query()

    def delete(self):
        pass

    def read(self):
        pass

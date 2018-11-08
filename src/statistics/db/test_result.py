from enum import Enum, auto
from uuid import UUID

from src.statistics.db.entity import Entity


class TestResult(Entity):
    class NoisesType(Enum):
        SINGLE = auto()
        BLOCK = auto()

    timestamp: int
    cascade: bool
    first_coder: UUID
    second_coder: UUID
    type_of_noise: NoisesType
    noise: float

    def create(self):
        pass

    def delete(self):
        pass

    def read(self):
        pass

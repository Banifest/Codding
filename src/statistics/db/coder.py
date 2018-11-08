from enum import Enum, auto
from uuid import UUID

from src.statistics.db.entity import Entity


class Coder(Entity):
    class CodersType(Enum):
        HEMMING = auto()
        CYCLICAL = auto()
        CONVOLUTION = auto()
        FOUNTAIN = auto()

    guid: UUID
    coder_description: str
    type_of_coder: CodersType
    coder_speed: int
    len_input_information: int
    len_additional_information: int
    interleaver: bool

    def create(self):
        pass

    def delete(self):
        pass

    def read(self):
        pass

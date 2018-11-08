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
        self._connection.query("""
                    INSERT INTO Coder(guid, coder_description, type_of_coder, coder_speed, len_input_information, len_additional_information, interleaver)
                    VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6});
                """.format(
            self.guid,
            self.coder_description,
            self.type_of_coder,
            self.coder_speed,
            self.len_input_information,
            self.len_additional_information,
            self.interleaver
        ))

    def delete(self):
        self._connection.query("""
            DELETE FROM Coder
            WHERE guid = {0}
              AND coder_description = {1}}
              AND type_of_coder = {2}}
              AND coder_speed = {3}
              AND len_input_information = {4}
              AND len_additional_information = {5}
              AND interleaver = {6};
        """.format(
            self.guid,
            self.coder_description,
            self.type_of_coder,
            self.coder_speed,
            self.len_input_information,
            self.len_additional_information,
            self.interleaver
        ))

    def read(self):
        self._prepare_selection_statement()

    def save(self):
        pass


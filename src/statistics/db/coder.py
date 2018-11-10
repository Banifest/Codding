from enum import Enum, auto
from uuid import UUID

from src.statistics.db.entity import Entity


class Coder(Entity):
    TABLE_NAME: str = "Coder"

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

    def __init__(
            self,
            guid,
            coder_description,
            type_of_coder,
            coder_speed,
            len_input_information,
            len_additional_information,
            interleaver
    ):
        super().__init__()
        self.guid = guid
        self.coder_description = coder_description
        self.type_of_coder = type_of_coder
        self.coder_speed = coder_speed
        self.len_input_information = len_input_information
        self.len_additional_information = len_additional_information
        self.interleaver = interleaver

    def create(self):
        self._connection.query(f"""
                    INSERT INTO "Coder"(
                        "GUID", 
                        description, 
                        coder_type, 
                        coder_speed, 
                        input_length, 
                        additional_length, 
                        interleaver
                    )  VALUES (
                    {self.guid}, 
                    {self.coder_description}, 
                    {self.type_of_coder}, {self.coder_speed}, 
                    {self.len_input_information}, 
                    {self.len_additional_information}, 
                    {self.interleaver}
                    )
                """)

    def delete(self):
        self._connection.query(f"""
            DELETE FROM "Coder"
            WHERE "GUID" = {self.guid}
              AND description = {self.coder_description}
              AND coder_type = {self.type_of_coder}
              AND coder_speed = {self.coder_speed}
              AND input_length = {self.len_input_information}
              AND additional_length = {self.len_additional_information}
              AND interleaver = {self.interleaver};
        """)

    def read(self) -> list:
        return self._prepare_selection_statement(Coder.TABLE_NAME)


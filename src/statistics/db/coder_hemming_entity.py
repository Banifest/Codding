# coding=utf-8
from uuid import UUID

from src.statistics.db.coderentity import CoderEntity


class CoderEntity(CoderEntity):
    matrix_of_transformation: list

    def __init__(
            self,
            guid: UUID,
            coder_description: str,
            type_of_coder: CoderEntity.CodersType,
            coder_speed: int,
            len_input_information: int,
            len_additional_information: int,
            interleaver: bool,
            matrix_of_transformation: list
    ):
        super().__init__(
            guid,
            coder_description,
            type_of_coder,
            coder_speed,
            len_input_information,
            len_additional_information,
            interleaver
        )
        self.matrix_of_transformation = matrix_of_transformation

    def create(self):
        super().create()

        self._connection.query(f"""
                    INSERT INTO "Hemming"(
                        coder, 
                        matrix
                    )  VALUES (
                    '{self.guid}',
                    {self.matrix_of_transformation}                     
                    )
                """)

    def delete(self):
        super().delete()

    def read(self) -> list:
        return super().read()

from enum import Enum, auto

from src.statistics.db.coder import Coder
from src.statistics.db.entity import Entity


class TestResult(Entity):
    TABLE_NAME: str = "TestResult"

    class NoisesType(Enum):
        SINGLE = auto()
        BLOCK = auto()

    timestamp: int
    flg_cascade: bool
    first_coder: Coder
    second_coder: Coder
    type_of_noise: NoisesType
    noise: float

    def create(self):
        self._connection.query(f"""
                            INSERT INTO "TestResult"(
                                "Timestamp", 
                                first_coder, 
                                second_coder, 
                                flg_cascade, 
                                noise_type, 
                                noise
                            )  VALUES (
                            {self.timestamp}, 
                            {self.first_coder.guid}, 
                            {self.second_coder.guid}, 
                            {self.flg_cascade}, 
                            {self.type_of_noise}, 
                            {self.noise}
                            )
                        """)

    def delete(self):
        self._connection.query(f"""
            DELETE FROM "TestResult"
            WHERE "Timestamp" = {self.timestamp}
              AND first_coder = {self.first_coder.guid}
              AND second_coder  = {self.second_coder.guid}
              AND flg_cascade = {self.flg_cascade}
              AND noise_type  = {self.type_of_noise}
              AND noise  = {self.noise};
        """)

    def read(self) -> list:
        return self._connection.query(f"""
        SELECT *
        FROM {TestResult.TABLE_NAME};        
    """)

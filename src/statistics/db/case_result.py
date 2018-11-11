from uuid import UUID

from src.statistics.db.entity import Entity


class CaseResult(Entity):
    TABLE_NAME: str = "CaseResultTest"
    guid: UUID
    test_timestamp: int
    quantity_correct_bit: int
    quantity_incorrect_bit: int
    quantity_repair_bit: int
    quantity_changed_bit: int

    def __init__(
            self,
            guid,
            test_timestamp,
            quantity_correct_bit,
            quantity_incorrect_bit,
            quantity_repair_bit,
            quantity_changed_bit
    ):
        self.guid = guid
        self.test_timestamp = test_timestamp
        self.quantity_correct_bit = quantity_correct_bit
        self.quantity_incorrect_bit = quantity_incorrect_bit
        self.quantity_repair_bit = quantity_repair_bit
        self.quantity_changed_bit = quantity_changed_bit

    def create(self):
        self._connection.query(f"""
                            INSERT INTO "CaseResult"(
                                "GUID", 
                                test_timestamp, 
                                count_correct_bits, 
                                count_incorrect_bits, 
                                count_repair_bits, 
                                count_changed_bits
                            )  VALUES (
                            '{self.guid}', 
                            '{self.test_timestamp}', 
                            {self.quantity_correct_bit}, 
                            {self.quantity_incorrect_bit}, 
                            {self.quantity_repair_bit}, 
                            {self.quantity_changed_bit}
                            )
                        """)

    def delete(self):
        self._connection.query(f"""
            DELETE FROM "CaseResult"
            WHERE "GUID" = '{self.guid}';
        """)

    def read(self) -> list:
        return self._connection.query(f"""
        SELECT *
        FROM {CaseResult.TABLE_NAME};        
    """)

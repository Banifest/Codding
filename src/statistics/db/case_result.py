from uuid import UUID

from src.statistics.db.entity import Entity


class CaseResult(Entity):
    TABLE_NAME: str = "CaseResult"
    guid: UUID
    test_timestamp: int
    quantity_correct_bit: int
    quantity_incorrect_bit: int
    quantity_repair_bit: int
    quantity_changed_bit: int

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
                            {self.guid}, 
                            {self.test_timestamp}, 
                            {self.quantity_correct_bit}, 
                            {self.quantity_incorrect_bit}, 
                            {self.quantity_repair_bit}, 
                            {self.quantity_changed_bit}
                            )
                        """)

    def delete(self):
        self._connection.query(f"""
            DELETE FROM "CaseResult"
            WHERE "GUID" = {self.guid}
              AND test_timestamp = {self.test_timestamp}
              AND count_correct_bits  = {self.quantity_correct_bit}
              AND count_incorrect_bits = {self.quantity_incorrect_bit}
              AND count_repair_bits  = {self.quantity_repair_bit}
              AND count_changed_bits  = {self.quantity_changed_bit};
        """)

    def read(self) -> list:
        return self._connection.query(f"""
        SELECT *
        FROM {CaseResult.TABLE_NAME};        
    """)

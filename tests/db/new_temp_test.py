import datetime
import unittest
import uuid

from src.statistics.db.coderentity import CoderEntity
from src.statistics.db.connector import Connector
from src.statistics.db.table import coder_table, result_table, case_table


class MyTestCase(unittest.TestCase):
    def test_something(self):
        connection = Connector().get_connection()

        # Создание первого кодера
        first_coder_guid = uuid.uuid4()
        connection.execute(coder_table.insert().values(
            guid=first_coder_guid,
            coder_type=CoderEntity.CodersType.HEMMING.value,
            coder_speed=1,
            input_length=1,
            additional_length=1,
            # TODO add interleaver determining
            interleaver=False,
            description="test"
        ))

        timestamp = str(datetime.datetime.now())

        connection.execute(result_table.insert().values(
            timestamp=timestamp,
            flg_cascade=False,
            first_coder=first_coder_guid,
            second_coder=None,
            type_of_noise=1,
            noise=float(1.0)
        ))

        connection.execute(case_table.insert().values(
            guid=uuid.uuid4(),
            test_timestamp=timestamp,
            count_correct_bits=1,
            count_incorrect_bits=1,
            count_repair_bits=1,
            count_changed_bits=1
        ))


if __name__ == '__main__':
    unittest.main()

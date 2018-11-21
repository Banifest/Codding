import datetime
import time
import unittest
from uuid import UUID

from src.statistics.db.case_result_entity import CaseResultEntity


class CaseResultTest(unittest.TestCase):
    def test_create(self):
        case_result = CaseResultEntity(
            guid=UUID('{ba9763d0c10045a4b9511bf2df9302b2}'),
            test_timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
            quantity_correct_bit=1,
            quantity_incorrect_bit=1,
            quantity_repair_bit=1,
            quantity_changed_bit=1
        )
        case_result.create()
        case_result.save()
        pass

if __name__ == '__main__':
    unittest.main()

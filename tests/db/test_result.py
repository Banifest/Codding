import datetime
import time
import unittest
import uuid

from src.statistics.db.case_result import CaseResult
from src.statistics.db.coder import Coder
from src.statistics.db.test_result import TestResult


class TestResultTest(unittest.TestCase):
    def test_create(self):
        first = uuid.uuid4()
        second = uuid.uuid4()
        f_coder = Coder(
            guid=first,
            coder_description='test',
            type_of_coder=Coder.CodersType.HEMMING,
            coder_speed=1,
            len_input_information=1,
            len_additional_information=1,
            interleaver=True
        )
        f_coder.create()
        s_coder = Coder(
            guid=second,
            coder_description='test',
            type_of_coder=Coder.CodersType.HEMMING,
            coder_speed=1,
            len_input_information=1,
            len_additional_information=1,
            interleaver=True
        )
        s_coder.create()

        l_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        test_result = TestResult(
            timestamp=l_timestamp,
            flg_cascade=False,
            first_coder=f_coder,
            second_coder=s_coder,
            type_of_noise=TestResult.NoisesType.SINGLE,
            noise=1.1
        )
        test_result.create()
        test_result.save()
        case_result = CaseResult(
            guid=uuid.uuid4(),
            test_timestamp=l_timestamp,
            quantity_correct_bit=1,
            quantity_incorrect_bit=1,
            quantity_repair_bit=1,
            quantity_changed_bit=1
        )
        case_result.create()

        pass

if __name__ == '__main__':
    unittest.main()

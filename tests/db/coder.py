import unittest
from uuid import UUID

from src.statistics.db.coder_entry import CoderEntry


class CoderTest(unittest.TestCase):

    def test_create(self):
        coder = CoderEntry(
            guid=UUID('{ba9763d0c10045a4b9511bf2df9302b2}'),
            coder_description='test',
            type_of_coder=CoderEntry.CodersType.HEMMING,
            coder_speed=1,
            len_input_information=1,
            len_additional_information=1,
            interleaver=True
        )
        coder.create()

        coder = CoderEntry(
            guid=UUID('{ba9763d0c10045a4b9511bf2df9302b2}'),
            coder_description='test',
            type_of_coder=CoderEntry.CodersType.HEMMING,
            coder_speed=1,
            len_input_information=1,
            len_additional_information=1,
            interleaver=True
        )
        coder.create()
        coder.save()
        pass


if __name__ == '__main__':
    unittest.main()

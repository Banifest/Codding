# coding=utf-8
import unittest
from uuid import UUID

from src.statistics.db.coder_entity import coder_entity


class CoderTest(unittest.TestCase):

    def test_create(self):
        coder = coder_entity(
            guid=UUID('{ba9763d0c10045a4b9511bf2df9302b2}'),
            coder_description='test',
            type_of_coder=coder_entity.CodersType.HEMMING,
            coder_speed=1,
            len_input_information=1,
            len_additional_information=1,
            interleaver=True
        )
        coder.create()

        coder = coder_entity(
            guid=UUID('{ba9763d0c10045a4b9511bf2df9302b2}'),
            coder_description='test',
            type_of_coder=coder_entity.CodersType.HEMMING,
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

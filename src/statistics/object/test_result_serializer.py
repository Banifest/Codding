import datetime
import json
import uuid

from src.coders.abstract_coder import AbstractCoder
from src.helper.pattern.singleton import Singleton
# noinspection PyMethodMayBeStatic
from src.statistics.db.case_result_entity import CaseResultEntity
from src.statistics.db.coderentity import CoderEntity
from src.statistics.db.connector import Connector
from src.statistics.db.test_result_entity import TestResultEntity


# noinspection PyMethodMayBeStatic
class TestResultSerializer(metaclass=Singleton):

    def serialize_to_db(self, test_result: dict, first_coder: AbstractCoder, second_coder: AbstractCoder = None):
        # Создание первого кодера
        first_coder_guid = uuid.uuid4()
        first_coder_entity = CoderEntity(
            guid=first_coder_guid,
            coder_description='test',
            type_of_coder=first_coder.type_of_coder,
            coder_speed=1,
            len_input_information=1,
            len_additional_information=1,
            interleaver=False
        )
        first_coder_entity.create()

        second_coder_entity = None
        if test_result['is_cascade']:
            second_coder_guid = uuid.uuid4()
            second_coder_entity = CoderEntity(
                guid=second_coder_guid,
                coder_description=second_coder.name,
                type_of_coder=second_coder.type_of_coder,
                coder_speed=1,
                len_input_information=1,
                len_additional_information=1,
                interleaver=False
            )
            second_coder_entity.create()

        for result_iter in test_result['test_cases']:
            timestamp = str(datetime.datetime.now())

            TestResultEntity(
                timestamp=timestamp,
                flg_cascade=test_result['is_cascade'],
                first_coder=first_coder_entity,
                second_coder=second_coder_entity,
                type_of_noise=TestResultEntity.NoisesType.SINGLE,
                noise=10
            ).create()

            quantity_test: int = 0
            for case_iter in result_iter['case']:
                CaseResultEntity(
                    guid=uuid.uuid4(),
                    test_timestamp=timestamp,
                    quantity_correct_bit=case_iter[quantity_test]['correct bits'],
                    quantity_incorrect_bit=case_iter[quantity_test]['error bits'],
                    quantity_repair_bit=1,
                    quantity_changed_bit=1
                ).create()
                quantity_test += 1

        Connector().save()

    def serialize_to_json(self, test_result: dict, file_name: str = "lastResult.json") -> None:
        open(file_name, "w", encoding='UTF-8').write(json.dumps(test_result, ensure_ascii=False))

# coding=utf-8
import datetime
import json
import uuid

from src.coders.abstract_coder import AbstractCoder
from src.helper.pattern.singleton import Singleton
# noinspection PyMethodMayBeStatic
from src.statistics.db.connector import Connector
from src.statistics.db.table import coder_table, result_table, case_table


# noinspection PyMethodMayBeStatic
class TestResultSerializer(metaclass=Singleton):

    def serialize_to_db(self, test_result: dict, first_coder: AbstractCoder, second_coder: AbstractCoder = None):
        connection = Connector().get_connection()

        # Создание первого кодера
        first_coder_guid = uuid.uuid4()
        connection.execute(coder_table.insert().values(
            guid=first_coder_guid,
            coder_type=first_coder.type_of_coder.value,
            coder_speed=first_coder.get_speed(),
            input_length=first_coder.lengthInformation,
            additional_length=first_coder.countAdditional,
            # TODO add interleaver determining
            interleaver=False,
            description=first_coder._name
        ))

        second_coder_guid = None
        if test_result['is_cascade']:
            second_coder_guid = uuid.uuid4()
            connection.execute(coder_table.insert().values(
                guid=second_coder_guid,
                coder_type=second_coder.type_of_coder.value,
                coder_speed=second_coder.get_speed(),
                input_length=second_coder.lengthInformation,
                additional_length=second_coder.countAdditional,
                # TODO add interleaver determining
                interleaver=False,
                description=second_coder.name
            ))

        # TODO необходимо разделить на объекты
        if "auto_test_information" in test_result:
            current_noise: float = test_result["auto_test_information"]["start"]
        else:
            return
            # TODO необходимо добавить для одиновного теста логику
        #            quantity_test: int = 0
        #            current_noise: float = 1
        #            timestamp = str(datetime.datetime.now())
        #            for case_iter in test_result["test"]:
        #                connection.execute(case_table.insert().values(
        #                    guid=uuid.uuid4(),
        #                    test_timestamp=timestamp,
        #                    count_correct_bits=case_iter[quantity_test]['correct bits'],
        #                    count_incorrect_bits=case_iter[quantity_test]['error bits'],
        #                    count_repair_bits=case_iter[quantity_test]['repair bits'],
        #                    count_changed_bits=case_iter[quantity_test]['change bits']
        #                ))
        #
        #                quantity_test += 1

        for result_iter in test_result['test_cases']:
            timestamp = str(datetime.datetime.now())

            connection.execute(result_table.insert().values(
                timestamp=timestamp,
                flg_cascade=test_result['is_cascade'],
                first_coder=first_coder_guid,
                second_coder=second_coder_guid,
                type_of_noise=1,
                noise=current_noise
            ))
            current_noise += test_result["auto_test_information"]["step"]

            quantity_test: int = 0
            for case_iter in result_iter['case']:
                connection.execute(case_table.insert().values(
                    guid=uuid.uuid4(),
                    test_timestamp=timestamp,
                    count_correct_bits=case_iter[quantity_test]['correct bits'],
                    count_incorrect_bits=case_iter[quantity_test]['error bits'],
                    count_repair_bits=case_iter[quantity_test]['repair bits'],
                    count_changed_bits=case_iter[quantity_test]['change bits']
                ))

                quantity_test += 1

    def serialize_to_json(self, test_result: dict, file_name: str = "lastResult.json") -> None:
        open(file_name, "w", encoding='UTF-8').write(json.dumps(test_result, ensure_ascii=False))

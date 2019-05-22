# coding=utf-8
import datetime
import uuid

import jsonpickle

from src.coders.abstract_coder import AbstractCoder
from src.helper.pattern.singleton import Singleton
from src.statistics.db.connector import Connector
from src.statistics.db.table import coder_table, result_table, case_table
from src.statistics.object.statistic_collector import StatisticCollector


# noinspection PyMethodMayBeStatic
class TestResultSerializer(metaclass=Singleton):

    def serialize_to_db(self, statistic_collector: StatisticCollector):
        connection = Connector().get_connection()

        # Generate UUID first _coder
        first_coder_guid = uuid.uuid4()
        first_coder: AbstractCoder = statistic_collector.firstCoder
        connection.execute(coder_table.insert().values(
            guid=first_coder_guid,
            coder_type=first_coder.typeOfCoder.value,
            coder_speed=first_coder.get_speed(),
            input_length=first_coder.lengthInformation,
            additional_length=first_coder.countAdditional,
            interleaver=statistic_collector.lengthFirstInterleaver is not None,
            interleaver_length=statistic_collector.lengthFirstInterleaver,
            description=first_coder.name
        ))
        first_coder.save_to_database(
            coder_guid=first_coder_guid,
            connection=connection
        )
        # Generate second _coder
        if statistic_collector.flgCascade:
            second_coder_guid = uuid.uuid4()
            second_coder: AbstractCoder = statistic_collector.secondCoder
            connection.execute(coder_table.insert().values(
                guid=second_coder_guid,
                coder_type=second_coder.typeOfCoder.value,
                coder_speed=second_coder.get_speed(),
                input_length=second_coder.lengthInformation,
                additional_length=second_coder.countAdditional,
                interleaver=statistic_collector.lengthSecondInterleaver is not None,
                interleaver_length=statistic_collector.lengthFirstInterleaver,
                description=second_coder.name
            ))

            second_coder.save_to_database(
                coder_guid=second_coder_guid,
                connection=connection
            )
        else:
            second_coder_guid = None

        for result_iter in statistic_collector.testResult:
            timestamp = str(datetime.datetime.now())

            connection.execute(result_table.insert().values(
                timestamp=timestamp,
                flg_cascade=statistic_collector.flgCascade,
                first_coder=first_coder_guid,
                second_coder=second_coder_guid,
                type_of_noise=1,
                noise=result_iter.noise
            ))

            for case_iter in result_iter.list_case_result:
                connection.execute(case_table.insert().values(
                    guid=uuid.uuid4(),
                    test_timestamp=timestamp,
                    count_correct_bits=case_iter.successfulBits,
                    count_incorrect_bits=case_iter.errorBits,
                    count_repair_bits=case_iter.repairBits,
                    count_changed_bits=case_iter.changedBits
                ))

    def serialize_to_json(self, statistic_collector: StatisticCollector, file_name: str = "lastResult.json") -> None:
        open(file_name, "w", encoding='UTF-8').write(jsonpickle.encode(statistic_collector, unpicklable=False))

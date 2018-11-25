from typing import Optional, List

from src.coders.abstract_coder import AbstractCoder


class CaseResult:

    def __init__(
            self,
            successful_bits: int,
            repair_bits: int,
            changed_bits: int,
            error_bits: int
    ):
        self.error_bits = error_bits
        self.changed_bits = changed_bits
        self.repair_bits = repair_bits
        self.successful_bits = successful_bits


class TestResult:

    def __init__(
            self,
            list_case_result: List[CaseResult],
            first_coder: AbstractCoder,
            second_coder: Optional[AbstractCoder],
            noise_type: int,
            flg_cascade: bool
    ):
        self.flg_cascade = flg_cascade
        self.noise_type = noise_type
        self.second_coder = second_coder
        self.first_coder = first_coder
        self.list_case_result = list_case_result


class StatisticCollect:
    flg_cascade: bool
    first_coder: AbstractCoder
    second_coder: Optional[AbstractCoder]
    test_result: TestResult

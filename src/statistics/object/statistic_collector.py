# coding=utf-8
from dataclasses import dataclass
from typing import Optional, List

from src.channel.enum_noise_mode import EnumNoiseMode
from src.coders.abstract_coder import AbstractCoder


class CaseResult:
    successful_bits: int
    repair_bits: int
    changed_bits: int
    error_bits: int

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


@dataclass
class TestResult:
    list_case_result: List[CaseResult]
    first_coder: AbstractCoder
    second_coder: Optional[AbstractCoder]
    noise_type: EnumNoiseMode
    noise: float
    flg_cascade: bool
    successful_packages: int
    repair_packages: int
    changed_packages: int
    error_packages: int
    quantity_correct_bits: int
    quantity_error_bits: int
    based_correct_bits: int
    based_error_bits: int


class StatisticCollector:
    flgCascade: bool
    firstCoder: AbstractCoder
    secondCoder: Optional[AbstractCoder]
    testResult: List[TestResult]
    lengthFirstInterleaver: Optional[int]
    lengthSecondInterleaver: Optional[int]
    beginNoise: float
    endNoise: float
    quantity_of_steps_in_cycle: int

    def __init__(
            self,
            flg_cascade: bool,
            first_coder: AbstractCoder,
            second_coder: Optional[AbstractCoder],
            test_result: List[TestResult],
            length_first_interleaver: Optional[int],
            length_second_interleaver: Optional[int],
            begin_noise: float,
            end_noise: float,
            quantity_of_steps_in_cycle: int
    ) -> None:
        self.flgCascade = flg_cascade
        self.firstCoder = first_coder
        self.secondCoder = second_coder
        self.testResult = test_result
        self.lengthFirstInterleaver = length_first_interleaver
        self.lengthSecondInterleaver = length_second_interleaver
        self.beginNoise = begin_noise
        self.endNoise = end_noise
        self.quantity_of_steps_in_cycle = quantity_of_steps_in_cycle

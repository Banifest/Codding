# coding=utf-8
from dataclasses import dataclass
from typing import Optional, List

from src.channel.enum_noise_mode import EnumNoiseMode
from src.coders.abstract_coder import AbstractCoder


@dataclass
class CaseResult:
    successfulBits: int
    repairBits: int
    changedBits: int
    errorBits: int


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


@dataclass
class StatisticCollector:
    flgCascade: bool
    firstCoder: AbstractCoder
    secondCoder: Optional[AbstractCoder]
    testResult: List[TestResult]
    lengthFirstInterleaver: Optional[int]
    lengthSecondInterleaver: Optional[int]
    beginNoise: float
    endNoise: float
    quantityStepsInCycle: int

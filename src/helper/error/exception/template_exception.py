# coding=utf-8
from dataclasses import dataclass


@dataclass
class TemplateException:
    message: str
    long_message: str

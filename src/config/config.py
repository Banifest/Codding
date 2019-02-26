# coding=utf-8
from dataclasses import dataclass


@dataclass
class Config:
    @dataclass
    class DBSetting:
        url: str = ""
        login: str = ""
        password: str = ""
        flg_used: bool = False

    db_setting: DBSetting = DBSetting()

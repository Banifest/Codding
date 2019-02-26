# coding=utf-8
from dataclasses import dataclass


@dataclass
class Config:
    @dataclass
    class DBSetting:
        flg_used: bool = False
        database_name: str = ""
        login: str = ""
        password: str = ""
        address: str = ""
        port: str = ""

    db_setting: DBSetting = DBSetting()

from enum import Enum


class UIRoutes(str, Enum):
    LOGIN = '/log-in'
    SQL = '/sql'
    SQL_TRYSQL = '/sql/trysql.asp'

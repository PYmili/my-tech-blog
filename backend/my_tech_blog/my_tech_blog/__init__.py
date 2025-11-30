import pymysql

from utils import SensitiveWordCheck

pymysql.install_as_MySQLdb()

# 加载违禁词检测实例
SensitiveWordCheckInstance = SensitiveWordCheck.Instance
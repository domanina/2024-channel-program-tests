import atexit
import logging
from typing import Optional

import pymysql


logger = logging.getLogger("logger")


class DBClient:

    def __init__(self, server_name, db_name, username, password):
        self.connection = pymysql.connect(host=server_name, user=username, passwd=password, db=db_name, autocommit=True)
        atexit.register(self.connection.close)

    def execute_sql_query(self, query: str, params: Optional[tuple] = None):
        with self.connection.cursor() as cursor:
            result = []
            try:
                cursor.execute(query, params)
                logger.info("Executed SQL query: %s")
                result = cursor.fetchall()
            except pymysql.DatabaseError as e:
                logger.error("DB Error: %s.\nRolling back the transaction", e)
                self.connection.rollback()
                logger.debug("DB transaction rolled back")
                raise e
            except Exception as e:
                logger.error("Error: %s", e)
                raise e
        return result

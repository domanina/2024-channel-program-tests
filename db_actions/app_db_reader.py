from typing import List

from config.config import RDS_USERNAME, RDS_PASSWORD
from config.config import RDS_DATABASE_NAME, RDS_HOST
from db_actions.db_client import DBClient
from tools.logger import get_logger
from tools.singleton import Singleton

logger = get_logger(name="logger")


class AppDbReader(DBClient, metaclass=Singleton):
    def __init__(self, server_name, db_name, password, username):
        super().__init__(
            server_name=server_name,
            db_name=db_name,
            password=password,
            username=username
        )


def get_db_reader():
    return AppDbReader(
        server_name=RDS_HOST,
        db_name=RDS_DATABASE_NAME,
        password=RDS_PASSWORD,
        username=RDS_USERNAME
    )


def delete_test_data() -> List[dict]:
    db_reader = get_db_reader()
    select_query = """SELECT * FROM .... WHERE description LIKE %s"""
    delete_query = """DELETE FROM ... WHERE description LIKE %s"""
    prefix = 'dao-qa-%'

    try:
        rows_to_delete = db_reader.execute_sql_query(select_query, (prefix,))
        if rows_to_delete:
            db_reader.execute_sql_query(delete_query, (prefix,))
            logger.info(f"{len(rows_to_delete)} rows deleted.")
        else:
            logger.info("No rows found with name x")
        return rows_to_delete
    except Exception as e:
        logger.error(f"Error occurred while selecting and deleting rows: {e}")
        raise e


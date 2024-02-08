#!/usr/bin/env python3
"""
Filtered logger module
"""
import re
import logging
import os
import mysql.connector
from typing import List

PII_FIELDS: List[str] = ['name', 'email', 'phone', 'ssn', 'password']


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        for field in self.fields:
            message = re.sub(
                rf'{field}=.+?{self.SEPARATOR}',
                f'{field}={self.REDACTION}{self.SEPARATOR}',
                message
            )
        return message


def filter_datum(fields: list,
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Returns the log message with obfuscated fields.
    """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a logger object """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connection to the database """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    """ Retrieves data from the database and logs it """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    logger = get_logger()
    for row in cursor:
        message = "; ".join([
            f"{field}={str(value)}"
            for field, value
            in zip(cursor.column_names, row)])
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

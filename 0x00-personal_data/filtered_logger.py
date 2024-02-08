#!/usr/bin/env python3
"""
Filtered logger module
"""
import re


def filter_datum(
        fields: list,
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    Returns the log message with obfuscated fields.

    Arguments:
        fields: A list of strings representing all fields to obfuscate.
        redaction: A string representing by what the field will be obfuscated.
        message: A string representing the log line.
        separator: A string representing by which character
        is separating all fields in the log line (message).

    Returns:
        A string with obfuscated fields.
    """
    return re.sub(
            r'(?<={}=).*?(?={})'.format(separator, separator),
            redaction, message
            )

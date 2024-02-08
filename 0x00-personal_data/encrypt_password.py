#!/usr/bin/env python3

"""
Module encrypt_password contains functions
for hashing and validating passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password: A string representing the password to be hashed.

    Returns:
        A byte string representing the hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a password matches its hashed version.

    Args:
        hashed_password: A byte string representing the hashed password.
        password: A string representing the password to be checked.

    Returns:
        A boolean indicating whether the password matches its hashed version.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

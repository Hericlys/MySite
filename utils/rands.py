"""
Module responsible for generating random sequences
"""
from string import ascii_lowercase, digits
from random import SystemRandom
from django.utils.text import slugify


def random_letters(k: int = 5) -> str:
    """
    Generates a sequence of lowercase characters

    Parameters:
    k = int | Character string size

    Return: str
    """
    return ''.join(SystemRandom().choices(
        ascii_lowercase + digits,
        k=k,
    ))


def slugify_new(text: str) -> str:
    """
    Transforms text into slugify and adds a sequence of random characters to
    the end

    Parameters:
    text = str | text

    Return: str
    """
    return slugify(text) + '-' + random_letters()
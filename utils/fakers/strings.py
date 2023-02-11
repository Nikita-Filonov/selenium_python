from random import choice, randint
from string import ascii_letters, digits


def get_random_string(start: int = 9, end: int = 15) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(randint(start, end)))

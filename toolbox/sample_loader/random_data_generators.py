import random
import string


def random_digits(length: int):
    return ''.join(random.choice(string.digits) for _ in range(length))


def random_alpha_numeric(min_length: int, max_length: int):
    return ''.join(random.choice(string.ascii_lowercase + string.digits)
                   for _ in range(random.randint(min_length, max_length)))


def random_alphabetic(min_length: int, max_length: int):
    return ''.join(random.choice(string.ascii_lowercase)
                   for _ in range(random.randint(min_length, max_length)))


def random_characters(min_length: int, max_length: int):
    characters = ''.join(
        random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits + ',.-\"\'()&!/:')
        for _ in range(random.randint(min_length, max_length)))
    if characters.lstrip() != characters:
        characters = random.choice(string.ascii_uppercase) + characters[1:]
    if characters.rstrip() != characters:
        characters = characters[:-2] + random.choice(string.ascii_lowercase)
    return characters


def random_date():
    return '-'.join(
        (str(random.randint(1900, 2020)), str(random.randint(1, 12)).zfill(2), str(random.randint(1, 28)).zfill(2)))

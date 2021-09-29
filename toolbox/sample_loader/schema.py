from functools import partial

from toolbox.sample_loader.random_data_generators import random_characters, random_date, random_digits
from toolbox.sample_loader.validation_rules import in_set, mandatory, no_padding_whitespace, numeric

SCHEMA = (
    {
        "columnName": "schoolId",
        "rules": [mandatory(), no_padding_whitespace()],
        "generator": partial(random_digits, length=11)
    },
    {
        "columnName": "schoolName",
        "rules": [mandatory(), no_padding_whitespace()],
        "generator": partial(random_characters, min_length=4, max_length=64)
    },
    {
        "columnName": "childFirstName",
        "rules": [mandatory(), no_padding_whitespace()],
        "sensitive": True,
        "generator": partial(random_characters, min_length=2, max_length=20)
    },
    {
        "columnName": "childMiddleNames",
        "rules": [no_padding_whitespace()],
        "sensitive": True,
        "generator": partial(random_characters, min_length=2, max_length=20)
    },
    {
        "columnName": "childLastName",
        "rules": [mandatory(), no_padding_whitespace()],
        "sensitive": True,
        "generator": partial(random_characters, min_length=2, max_length=20)
    },
    {
        "columnName": "childDob",
        "rules": [no_padding_whitespace()],
        "sensitive": True,
        "generator": random_date
    },
    {
        "columnName": "mobileNumber",
        "rules": [mandatory(), numeric()],
        "sensitive": True,
        "generator": lambda: '07' + random_digits(9)
    },
    {
        "columnName": "emailAddress",
        "rules": [no_padding_whitespace()],
        "sensitive": True,
    },
    {
        "columnName": "consentGivenTest",
        "rules": [in_set({"true", "false"})],
        "sensitive": True,
        "generator": lambda: 'true'
    },
    {
        "columnName": "consentGivenSurvey",
        "rules": [in_set({"true", "false"})],
        "sensitive": True,
        "generator": lambda: 'true'
    }
)

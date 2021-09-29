from toolbox.sample_loader.validation_rules import mandatory

SCHEMA = (
    {
        "columnName": "schoolId",
        "rules": [mandatory()]
    },
    {
        "columnName": "schoolName",
        "rules": [mandatory()]
    },
    {
        "columnName": "childFirstName",
        "rules": [mandatory()],
        "sensitive": True
    },
    {
        "columnName": "childMiddleNames",
        "rules": [],
        "sensitive": True
    },
    {
        "columnName": "childLastName",
        "rules": [mandatory()],
        "sensitive": True
    },
    {
        "columnName": "childDob",
        "rules": [],
        "sensitive": True
    },
    {
        "columnName": "yearGroup",
        "rules": [],
        "sensitive": True
    },
    {
        "columnName": "mobileNumber",
        "rules": [mandatory()],
        "sensitive": True
    },
    {
        "columnName": "emailAddress",
        "rules": [],
        "sensitive": True
    },
)

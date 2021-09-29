from toolbox.sample_loader.validation_rules import mandatory, no_padding_whitespace, numeric, in_set

SCHEMA = (
    {
        "columnName": "schoolId",
        "rules": [mandatory(), no_padding_whitespace()]
    },
    {
        "columnName": "schoolName",
        "rules": [mandatory(), no_padding_whitespace()]
    },
    {
        "columnName": "childFirstName",
        "rules": [mandatory(), no_padding_whitespace()],
        "sensitive": True
    },
    {
        "columnName": "childMiddleNames",
        "rules": [no_padding_whitespace()],
        "sensitive": True
    },
    {
        "columnName": "childLastName",
        "rules": [mandatory(), no_padding_whitespace()],
        "sensitive": True
    },
    {
        "columnName": "childDob",
        "rules": [no_padding_whitespace()],
        "sensitive": True
    },
    {
        "columnName": "mobileNumber",
        "rules": [mandatory(), numeric()],
        "sensitive": True
    },
    {
        "columnName": "emailAddress",
        "rules": [no_padding_whitespace()],
        "sensitive": True
    },
    {
        "columnName": "consentGivenTest",
        "rules": [in_set({"true", "false"})],
        "sensitive": True
    },
    {
        "columnName": "consentGivenSurvey",
        "rules": [in_set({"true", "false"})],
        "sensitive": True
    }
)

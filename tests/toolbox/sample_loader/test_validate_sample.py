from pathlib import Path

from toolbox.sample_loader.validate_sample import SampleValidator

RESOURCE_FILE_PATH = Path(__file__).parents[2].joinpath('resources')


def test_validate_sample_success():
    # Given
    sample_validator = SampleValidator()
    valid_sample_file_path = RESOURCE_FILE_PATH.joinpath('valid_generated_sample_20.csv')

    # When
    validation_failures = sample_validator.validate(valid_sample_file_path)

    # Then
    assert not validation_failures, 'Should find no validation failures'


def test_validate_sample_invalid():
    # Given
    sample_validator = SampleValidator()
    invalid_sample_file_path = RESOURCE_FILE_PATH.joinpath('invalid_sample_missing_schoolId.csv')

    # When
    validation_failures = sample_validator.validate(invalid_sample_file_path)

    # Then
    assert len(validation_failures) == 1
    failure = validation_failures[0]
    assert failure.line_number == 2
    assert failure.columnName == 'schoolId'

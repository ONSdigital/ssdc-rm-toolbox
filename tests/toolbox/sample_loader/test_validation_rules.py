import pytest

from toolbox.sample_loader import validation_rules


def test_max_length_valid():
    # Given
    max_length_validator = validation_rules.max_length(10)

    # When
    max_length_validator('a' * 9)

    # Then no invalid exception is raised


def test_max_length_invalid():
    # Given
    max_length_0_validator = validation_rules.max_length(10)

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        max_length_0_validator('a' * 11)


def test_unique_valid():
    # Given
    unique_validator = validation_rules.unique()

    # When
    unique_validator('1')
    unique_validator('2')
    unique_validator('3')
    unique_validator('foo')
    unique_validator('bar')

    # Then no invalid exception is raised


def test_unique_invalid():
    # Given
    unique_validator = validation_rules.unique()

    # When
    unique_validator('1')
    unique_validator('2')
    unique_validator('3')
    unique_validator('foo')

    # Then raises
    with pytest.raises(validation_rules.Invalid):
        unique_validator('1')


def test_unique_validation_rules_do_not_cross_validate():
    # Given
    unique_validator_1 = validation_rules.unique()
    unique_validator_2 = validation_rules.unique()

    # When
    unique_validator_1('a')
    unique_validator_2('a')

    # Then no invalid exception is raised


def test_mandatory_valid():
    # Given
    mandatory_validator = validation_rules.mandatory()

    # When
    mandatory_validator('a')

    # Then no invalid exception is raised


def test_mandatory_invalid():
    # Given
    mandatory_validator = validation_rules.mandatory()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        mandatory_validator('')


def test_numeric_valid():
    # Given
    numeric_validator = validation_rules.numeric()

    # When
    numeric_validator('0123456789')

    # Then no invalid exception is raised


def test_numeric_invalid():
    # Given
    numeric_validator = validation_rules.numeric()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        numeric_validator('a')

    with pytest.raises(validation_rules.Invalid):
        numeric_validator('1.1')

    with pytest.raises(validation_rules.Invalid):
        numeric_validator('_')


def test_lat_long_valid():
    # Given
    lat_long_validator = validation_rules.latitude_longitude(max_scale=5, max_precision=10)

    # When
    lat_long_validator('1234.5678')

    # Then no invalid exception is raised


@pytest.mark.parametrize('value', [
    '1.1E-10',  # Python valid scientific notation
    '1.1e-10',
    '2e-4',
    '2E-4',
    '3E4',
    '3e5',
    '5.9238E-7',
    '0.2E-3',
    '23.4E-5',
    '1.2345E2',
    '1.2345*10^-3',  # Not python valid notation
    '1.2345*10**-3',
    '1.2345x10**-3',
    '1.2345x10^-3',
    'eggs',
    '12.34.56.789',
])
def test_lat_long_scientific_notation_invalid(value):
    # Given
    lat_long_validator = validation_rules.latitude_longitude(max_scale=5, max_precision=10)

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        lat_long_validator(value)


def test_lat_long_malformed_decimal():
    # Given
    lat_long_validator = validation_rules.latitude_longitude(max_scale=5, max_precision=10)

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        lat_long_validator('1')


def test_lat_long_invalid_format():
    # Given
    lat_long_validator = validation_rules.latitude_longitude(max_scale=5, max_precision=10)

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        lat_long_validator('foo')


def test_lat_long_invalid_scale():
    # Given
    lat_long_validator = validation_rules.latitude_longitude(max_scale=5, max_precision=10)

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        lat_long_validator('1.567889')


def test_lat_long_invalid_precision():
    # Given
    lat_long_validator = validation_rules.latitude_longitude(max_scale=10, max_precision=5)

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        lat_long_validator('123456.7')


def test_in_set_valid():
    # Given
    in_set_validator = validation_rules.in_set({'a', 'b', 'c'})

    # When
    in_set_validator('a')
    in_set_validator('b')
    in_set_validator('c')

    # Then no invalid exception is raised


def test_in_set_invalid():
    # Given
    in_set_validator = validation_rules.in_set({'a'})

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        in_set_validator('abc')


def test_set_equal_valid():
    # Given
    set_equal_validator = validation_rules.set_equal({'a', 'b', 'c'})

    # When
    set_equal_validator(['a', 'b', 'c'])

    # Then no invalid exception is raised


def test_set_equal_invalid():
    # Given
    set_equal_validator = validation_rules.set_equal({'a', 'b', 'c'})

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        set_equal_validator(['a', 'b', 'c', 'blah'])


def test_no_padding_whitespace_check_valid():
    # Given
    no_padding_whitespace_validator = validation_rules.no_padding_whitespace()

    # When
    no_padding_whitespace_validator('')

    # Then no invalid exception is raised


def test_no_padding_whitespace_check_invalid():
    # Given
    no_padding_whitespace_validator = validation_rules.no_padding_whitespace()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        no_padding_whitespace_validator('  ')


def test_no_pipe_character_check_valid():
    # Given
    no_pipe_character_validator = validation_rules.no_pipe_character()

    # When, then raises
    no_pipe_character_validator('test')

    # Then no invalid exception is raised


def test_no_pipe_character_check_invalid():
    # Given
    no_pipe_character_validator = validation_rules.no_pipe_character()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        no_pipe_character_validator('|')


def test_alphanumeric_postcode_valid():
    # Given
    alphanumeric_postcode_validator = validation_rules.alphanumeric_postcode()

    # When
    alphanumeric_postcode_validator('TE25 5TE')

    # Then no invalid exception is raised


def test_alphanumeric_postcode_invalid():
    # Given
    alphanumeric_postcode_validator = validation_rules.alphanumeric_postcode()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        alphanumeric_postcode_validator('TE5 5TE!')


def test_latitude_longitude_range_valid():
    # Given
    latitude_longitude_range_validator = validation_rules.latitude_longitude_range()

    # When
    latitude_longitude_range_validator(50)

    # Then no invalid exception is raised


def test_latitude_longitude_range_invalid():
    # Given
    latitude_longitude_range_validator = validation_rules.latitude_longitude_range()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        latitude_longitude_range_validator(360)


def test_alphanumeric_plus_hyphen_field_values_valid():
    # Given
    alphanumeric_plus_hyphen_field_validator = validation_rules.alphanumeric_plus_hyphen_field_values()

    # When
    alphanumeric_plus_hyphen_field_validator('TE-STT1-ES-01')

    # Then no invalid exception is raised


def test_alphanumeric_plus_hyphen_field_values_invalid():
    # Given
    alphanumeric_plus_hyphen_field_validator = validation_rules.alphanumeric_plus_hyphen_field_values()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        alphanumeric_plus_hyphen_field_validator('TE-STT1-ES-!!')


@pytest.mark.parametrize('value', [
    '07123456789',
    '07987654321',
    '07234534256',
])
def test_uk_mobile_number_valid(value):
    # Given
    uk_mobile_number_starting_07_validator = validation_rules.uk_mobile_number_starting_07()

    # When
    uk_mobile_number_starting_07_validator(value)

    # Then no Invalid exception is raised


@pytest.mark.parametrize('value', [
    'foo',
    '7123456789',
    '17123456789',
    '77123456789',
    '+447123456789',
    '0447123456789',
    'a7123456789',
    'a07123456789',
    '0712345678a',
])
def test_uk_mobile_number_invalid(value):
    # Given
    uk_mobile_number_starting_07_validator = validation_rules.uk_mobile_number_starting_07()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        uk_mobile_number_starting_07_validator(value)


def test_iso_date_valid():
    # Given
    iso_date_validator = validation_rules.iso_date()

    # When
    iso_date_validator('2021-10-11')

    # Then no invalid exception raised


def test_iso_date_invalid():
    # Given
    iso_date_validator = validation_rules.iso_date()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        iso_date_validator('66-666-6666')


def test_iso_datetime_valid():
    # Given
    iso_datetime_validator = validation_rules.iso_datetime()

    # When
    iso_datetime_validator('2021-10-11T12:00:00Z')

    # Then no invalid exception raised


def test_iso_datetime_invalid():
    # Given
    iso_datetime_validator = validation_rules.iso_datetime()

    # When, then raises
    with pytest.raises(validation_rules.Invalid):
        iso_datetime_validator('66-666-6666T66:66:66Z')

from typing import Iterable


class Invalid(Exception):
    pass


def max_length(max_len: int):
    def validate(value, **_kwargs):
        if len(value) > max_len:
            raise Invalid(f'Value has length {len(value)}, exceeds max of {max_len}')

    return validate


def unique():
    previous_values = set()

    def validate(value, **_kwargs):
        if value in previous_values:
            raise Invalid(f'Value "{value}" is not unique')
        previous_values.add(value)

    return validate


def mandatory():
    def validate(value, **_kwargs):
        if not value or value.replace(" ", "") == '':
            raise Invalid('Empty mandatory value')

    return validate


def numeric():
    def validate(value, **_kwargs):
        if value and value.replace(" ", "") == '':
            pass
        elif value and not value.replace(" ", "").isnumeric():
            raise Invalid(f'Value "{value}" is non numeric')

    return validate


def latitude_longitude(max_precision: int, max_scale: int):
    def validate(value, **_kwargs):
        try:
            float(value)
        except ValueError:
            raise Invalid(f'Value "{value}" is not a valid float')
        try:
            # This will fail validation correctly if given a value with none or multiple '.'s
            # as this line raises ValueError if it cannot unpack into 2 variables.
            integer, decimal = value.split('.')
            int(integer)
            int(decimal)
        except ValueError:
            raise Invalid(f'Malformed decimal, Value = "{value}"')
        integer = integer.strip('-')
        scale = len(decimal)
        precision = len(integer) + len(decimal)
        errors = []
        if precision > max_precision:
            errors.append(f'Precision {precision} exceeds max of {max_precision}')
        if scale > max_scale:
            errors.append(f'Scale {scale} exceeds max of {max_scale}')
        if errors:
            raise Invalid(f'{", ".join(errors)}, Value = "{value}"')

    return validate


def in_set(valid_value_set: set):
    def validate(value, **_kwargs):
        if value not in valid_value_set:
            raise Invalid(f'Value "{value}" is not in the valid set')

    return validate


def set_equal(expected_set):
    def validate(value: Iterable, **_kwargs) -> None:
        value_as_set = set(value)
        if value_as_set != expected_set:
            raise Invalid((f"Values don't match expected set, "
                           f'missing values: {expected_set.difference(value_as_set)}, '
                           f'unexpected values: {value_as_set.difference(expected_set)}'))

    return validate


def no_padding_whitespace():
    def validate(value, **_kwargs):
        if value != value.strip():
            raise Invalid(f'Value "{value}" contains padding whitespace')

    return validate


def no_pipe_character():
    def validate(value, **_kwargs):
        if str('|') in value:
            raise Invalid(f'Value "{value}" contains pipe character')

    return validate


def alphanumeric_postcode():
    def validate(postcode, **_kwargs):
        stripped_postcode = postcode.replace(" ", "")
        if not stripped_postcode.isalnum():
            raise Invalid(f'Postcode "{postcode}" is non alphanumeric')

    return validate


def alphanumeric_plus_hyphen_field_values():
    def validate(value, **_kwargs):
        stripped_field_value = value.replace("-", "")
        if not stripped_field_value.isalnum():
            raise Invalid(f'Value "{value}" contains invalid characters')

    return validate


def latitude_longitude_range():
    def validate(value, **_kwargs):
        try:
            lat_long_float = float(value)
        except ValueError:
            raise Invalid(f'Value "{value}" is not a valid float')
        if not -180 <= lat_long_float <= 180:
            raise Invalid(f'Latitude/Longitude value "{value}" is not in a range between -180 and 180')

    return validate


def uk_mobile_number_starting_07():
    def validate(value, **_kwargs):
        if value:
            try:
                int(value)
            except ValueError:
                raise Invalid(f'Value "{value}" is not a valid uk mobile number')
            if len(value) != 11 or value[:2] != '07':
                raise Invalid(f'Value "{value}" is not a valid uk mobile number')

    return validate

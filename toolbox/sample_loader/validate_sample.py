import argparse
import csv
from collections import namedtuple
from pathlib import Path

from toolbox.sample_loader.schema import SCHEMA
from toolbox.sample_loader.validation_rules import Invalid, set_equal

ValidationFailure = namedtuple('ValidationFailure', ('line_number', 'columnName', 'description'))


class SampleValidator:
    def __init__(self, schema):
        self.schema = schema

    def find_header_validation_failures(self, header):
        valid_header = set(column['columnName'] for column in self.schema)
        try:
            set_equal(valid_header)(header)
        except Invalid as invalid:
            return ValidationFailure(line_number=1, columnName=None, description=str(invalid))

    def find_row_validation_failures(self, line_number, row):
        failures = []
        for column in self.schema:
            for rule in column["rules"]:
                try:
                    rule(row[column['columnName']], row=row)
                except Invalid as invalid:
                    failures.append(ValidationFailure(line_number, column['columnName'], invalid))
        return failures

    def find_sample_validation_failures(self, sample_file_reader) -> list:
        failures = []
        for line_number, row in enumerate(sample_file_reader, 2):
            failures.extend(self.find_row_validation_failures(line_number, row))
            if not line_number % 10000:
                print(f"Validation progress: {str(line_number).rjust(8)} lines checked, "
                      f"Failures: {len(failures)}", end='\r', flush=True)
        print(f"Validation progress: {str(line_number).rjust(8)} lines checked, "
              f"Failures: {len(failures)}")
        return failures

    def validate(self, sample_file_path) -> list:
        try:
            with open(sample_file_path, encoding="utf-8") as sample_file:
                sample_file_reader = csv.DictReader(sample_file, delimiter=',')
                header_failures = self.find_header_validation_failures(sample_file_reader.fieldnames)
                if header_failures:
                    return [header_failures]
                return self.find_sample_validation_failures(sample_file_reader)
        except UnicodeDecodeError as err:
            return [
                ValidationFailure(line_number=None, column=None,
                                  description=f'Invalid file encoding, requires utf-8, error: {err}')]


def build_failure_log(failure):
    if failure.column:
        return f'line: {failure.line_number}, column: {failure.column}, description: {failure.description}'
    if failure.line_number:
        return f'line: Header, description: {failure.description}'
    return failure.description


def print_failures_summary(failures, print_limit):
    for failure in failures[:print_limit]:
        print(build_failure_log(failure))
    response = input(f'Showing first {print_limit} of {len(failures)}. '
                     f'Show remaining {len(failures) - print_limit} [Y/n]?\n')
    if response.lower() in {'y', 'yes'}:
        for failure in failures[print_limit:]:
            print(build_failure_log(failure))


def print_failures(failures, print_limit=20):
    print(f'{len(failures)} validation failure(s):')
    if len(failures) > print_limit:
        print_failures_summary(failures, print_limit)
    else:
        for failure in failures:
            print(build_failure_log(failure))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=Path)
    return parser.parse_args()


def main():
    args = parse_arguments()
    failures = SampleValidator(SCHEMA).validate(args.sample_file_path)
    if failures:
        print_failures(failures)
        print(f'{args.sample_file_path} is not valid ❌')
        exit(1)
    print(f'Success! {args.sample_file_path} passed validation ✅')


if __name__ == "__main__":
    main()

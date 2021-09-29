import argparse
import csv
import random
import string
from functools import partial
from pathlib import Path


class SampleGenerator:

    def __init__(self):
        self.schema = (
            {
                "columnName": "schoolId",
                "generator": partial(self.random_digits, length=11)
            },
            {
                "columnName": "schoolName",
                "generator": partial(self.random_characters, min_length=4, max_length=64)
            },
            {
                "columnName": "childFirstName",
                "generator": partial(self.random_characters, min_length=2, max_length=20)
            },
            {
                "columnName": "childMiddleNames",
                "generator": partial(self.random_characters, min_length=2, max_length=20)
            },
            {
                "columnName": "childLastName",
                "generator": partial(self.random_characters, min_length=2, max_length=20)
            },
            {
                "columnName": "childDob",
                "generator": self.random_date
            },
            {
                "columnName": "mobileNumber",
                "generator": lambda: '07' + self.random_digits(9)
            },
            {
                "columnName": "emailAddress",
            },
            {
                "columnName": "consentGivenTest",
                "generator": lambda: 'true'
            },
            {
                "columnName": "consentGivenSurvey",
                "generator": lambda: 'true'
            }

        )

        self.fieldnames = tuple(column['columnName'] for column in self.schema)

    def generate_sample_file(self, sample_size: int, output_file_path: Path):
        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=self.fieldnames)
            writer.writeheader()

            for row in range(sample_size):
                random_sample_row = {}
                for column in self.schema:
                    if column.get('generator'):
                        random_sample_row[column['columnName']] = column['generator']()
                writer.writerow(random_sample_row)

    @staticmethod
    def random_digits(length: int):
        return ''.join(random.choice(string.digits) for _ in range(length))

    @staticmethod
    def random_alpha_numeric(min_length: int, max_length: int):
        return ''.join(random.choice(string.ascii_lowercase + string.digits)
                       for _ in range(random.randint(min_length, max_length)))

    @staticmethod
    def random_alphabetic(min_length: int, max_length: int):
        return ''.join(random.choice(string.ascii_lowercase)
                       for _ in range(random.randint(min_length, max_length)))

    @staticmethod
    def random_characters(min_length: int, max_length: int):
        random_characters = ''.join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits + ',.-\"\'()&!/:')
            for _ in range(random.randint(min_length, max_length)))
        if random_characters.lstrip() != random_characters:
            random_characters = random.choice(string.ascii_uppercase) + random_characters[1:]
        if random_characters.rstrip() != random_characters:
            random_characters = random_characters[:-2] + random.choice(string.ascii_lowercase)
        return random_characters

    @staticmethod
    def random_date():
        return '-'.join(
            (str(random.randint(1900, 2020)), str(random.randint(1, 12)).zfill(2), str(random.randint(1, 28)).zfill(2)))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_size', help='Number of sample rows to generate', type=int)
    parser.add_argument('output_file_path', help='Path to write the generated file to', type=Path)
    return parser.parse_args()


def main():
    args = parse_arguments()
    SampleGenerator().generate_sample_file(args.sample_size, args.output_file_path)


if __name__ == "__main__":
    main()

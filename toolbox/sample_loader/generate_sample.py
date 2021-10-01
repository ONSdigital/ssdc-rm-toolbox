import argparse
import csv
from pathlib import Path

from toolbox.sample_loader.schema import SCHEMA


class SampleGenerator:

    def __init__(self, schema):
        self.schema = schema
        self.fieldnames = tuple(column['columnName'] for column in self.schema)

    def generate_sample_file(self, sample_size: int, output_file_path: Path):
        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=self.fieldnames)
            writer.writeheader()

            for _ in range(sample_size):
                random_sample_row = {}
                for column in self.schema:
                    if column.get('generator'):
                        random_sample_row[column['columnName']] = column['generator']()
                writer.writerow(random_sample_row)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_size', help='Number of sample rows to generate', type=int)
    parser.add_argument('output_file_path', help='Path to write the generated file to', type=Path)
    return parser.parse_args()


def main():
    args = parse_arguments()
    SampleGenerator(SCHEMA).generate_sample_file(args.sample_size, args.output_file_path)


if __name__ == "__main__":
    main()

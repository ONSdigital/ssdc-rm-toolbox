import argparse
import csv
import json
import logging
import os
import sys
import uuid
from typing import Iterable

from rabbit_context import RabbitContext

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    parser.add_argument('collection_exercise_id', help='collection exercise ID', type=str)
    return parser.parse_args()


def load_sample_file(sample_file_path, collection_exercise_id,
                     store_loaded_sample_units=False, **kwargs):
    with open(sample_file_path) as sample_file:
        return load_sample(sample_file, collection_exercise_id, store_loaded_sample_units, **kwargs)


def load_sample(sample_file: Iterable[str], collection_exercise_id: str,
                store_loaded_sample_units=False, **kwargs):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    return _load_sample_units(collection_exercise_id, sample_file_reader, store_loaded_sample_units,
                              **kwargs)


def _load_sample_units(collection_exercise_id: str, sample_file_reader: Iterable[str],
                       store_loaded_sample_units=False, sample_unit_log_frequency=5000, **kwargs):
    sample_units = {}

    with RabbitContext(**kwargs) as rabbit:
        logger.info(f'Loading sample units to queue {rabbit.queue_name}')

        for count, sample_row in enumerate(sample_file_reader, 1):
            sample_unit_id = uuid.uuid4()

            rabbit.publish_message(_create_case_json(sample_row, collection_exercise_id=collection_exercise_id),
                                   content_type='application/json')

            if store_loaded_sample_units:
                sample_unit = {
                    f'sampleunit:{sample_unit_id}': _create_sample_unit_json(sample_unit_id, sample_row)}
                sample_units.update(sample_unit)

            if count % sample_unit_log_frequency == 0:
                logger.info(f'{count} sample units loaded')

        if count % sample_unit_log_frequency:
            logger.info(f'{count} sample units loaded')

    logger.info(f'All sample units have been added to the queue {rabbit.queue_name}')

    return sample_units


def _create_case_json(sample_row, collection_exercise_id) -> str:
    create_case = {
        'caseId': str(uuid.uuid4()),
        'collectionExerciseId': collection_exercise_id,
        'sample': sample_row
    }

    return json.dumps(create_case)


def _create_sample_unit_json(sample_unit_id, sample_unit) -> str:
    sample_unit = {'id': str(sample_unit_id), 'attributes': sample_unit}
    return json.dumps(sample_unit)


def main():
    log_level = os.getenv('LOG_LEVEL')
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=log_level or logging.ERROR)
    logger.setLevel(log_level or logging.INFO)
    args = parse_arguments()
    load_sample_file(args.sample_file_path, args.collection_exercise_id,
                     store_loaded_sample_units=False)


if __name__ == "__main__":
    main()

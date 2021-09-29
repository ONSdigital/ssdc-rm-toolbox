import argparse
import csv
import json
import logging
import os
import sys
import uuid
from typing import Iterable, Mapping

from google.cloud import pubsub_v1

from toolbox.config import Config
from toolbox.sample_loader.schema import SCHEMA

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SampleLoader:
    def __init__(self, schema, collection_exercise_id, sample_unit_log_frequency=5000, publish_timeout=60):
        self.schema = schema
        self.sample_keys = {column['columnName'] for column in self.schema if not column.get('sensitive')}
        self.sample_sensitive_keys = {column['columnName'] for column in self.schema if column.get('sensitive')}
        self.collection_exercise_id = collection_exercise_id
        self.sample_unit_log_frequency = sample_unit_log_frequency
        self.publish_timeout = publish_timeout

    def load_sample_file(self, sample_file_path):
        with open(sample_file_path) as sample_file:
            return self.load_sample(sample_file)

    def load_sample(self, sample_file: Iterable[str]):
        sample_file_reader = csv.DictReader(sample_file, delimiter=',')
        return self._load_sample_units(sample_file_reader)

    def _load_sample_units(self, sample_file_reader: Iterable[Mapping]):

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(Config.SHARED_PROJECT_ID, Config.NEW_CASE_TOPIC)
        logger.info(f'Publishing sample units to topic {Config.NEW_CASE_TOPIC}')

        for count, sample_row in enumerate(sample_file_reader, 1):

            future = publisher.publish(
                topic_path,
                self.create_new_case_event(sample_row)
            )

            # Block until finished publishing
            try:
                future.result(timeout=self.publish_timeout)
            except:
                logger.error(
                    f'Failed to publish new case message on row {count} on within timeout ({self.publish_timeout}s)')
                raise

            if count % self.sample_unit_log_frequency == 0:
                logger.info(f'{count} sample units published')

        if count % self.sample_unit_log_frequency:
            logger.info(f'{count} sample units published')

        logger.info(f'All sample units have been published to the topic {Config.NEW_CASE_TOPIC}')

    def create_new_case_event(self, sample_row) -> bytes:
        sample_fields = {key: value for key, value in sample_row.items() if key in self.sample_keys}
        sample_sensitive_fields = {key: value for key, value in sample_row.items() if key in self.sample_sensitive_keys}

        new_case_event = {
            'header': {
                'version': Config.EVENT_SCHEMA_VERSION,
                'topic': Config.NEW_CASE_TOPIC,
                'source': Config.SERVICE_NAME,
                'channel': Config.EVENT_CHANNEL,
                'dateTime': '2020-01-01T01:02:03Z',  # TODO
                'messageId': str(uuid.uuid4()),
                'correlationId': str(uuid.uuid4()),
                'originatingUser': Config.CURRENT_USER
            },
            'newCase': {
                'caseId': str(uuid.uuid4()),
                'collectionExerciseId': str(self.collection_exercise_id),
                'sample': sample_fields,
                'sampleSensitive': sample_sensitive_fields
            }
        }
        return json.dumps(new_case_event).encode('utf-8')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    parser.add_argument('collection_exercise_id', help='collection exercise ID', type=str)
    return parser.parse_args()


def main():
    log_level = os.getenv('LOG_LEVEL')
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=log_level or logging.ERROR)
    logger.setLevel(log_level or logging.INFO)
    args = parse_arguments()
    SampleLoader(SCHEMA, args.collection_exercise_id).load_sample_file(args.sample_file_path)


if __name__ == "__main__":
    main()

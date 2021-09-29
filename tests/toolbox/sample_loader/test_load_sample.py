import json
import uuid
from unittest.mock import patch

from toolbox.config import Config
from toolbox.sample_loader.load_sample import SampleLoader

TEST_SCHEMA = (
    {
        "columnName": "foo",
        "rules": [],
    },
    {
        "columnName": "spam",
        "rules": [],
        "sensitive": True
    },
)
TEST_HEADER = tuple(column['columnName'] for column in TEST_SCHEMA)


@patch('toolbox.sample_loader.load_sample.pubsub_v1')
def test_load_sample_publishes_new_case_events(patched_pubsub):
    # Given
    collection_exercise_id = uuid.uuid4()
    sample_loader = SampleLoader(TEST_SCHEMA, collection_exercise_id)

    sample_file = (f"{','.join(TEST_HEADER)}\n",
                   "bar,eggs\n",
                   "hoo,har\n")

    # When
    sample_loader.load_sample(sample_file)

    # Then
    patched_publish = patched_pubsub.PublisherClient.return_value.publish
    patched_publish_future = patched_publish.return_value

    assert patched_publish.call_count == 2, 'Expected 2 calls to publish message'

    published = patched_publish.call_args_list
    first_published_message = json.loads(published[0][0][1])
    assert first_published_message.get('newCase').get('sample') == {"foo": "bar"}
    assert first_published_message.get('newCase').get('sampleSensitive') == {"spam": "eggs"}

    second_published_message = json.loads(published[1][0][1])
    assert second_published_message.get('newCase').get('sample') == {"foo": "hoo"}
    assert second_published_message.get('newCase').get('sampleSensitive') == {"spam": "har"}

    assert patched_publish_future.result.call_count == 2, 'Expected 2 calls to get result of publish future'


def test_create_new_case_event():
    # Given
    collection_exercise_id = uuid.uuid4()
    sample_loader = SampleLoader(TEST_SCHEMA, collection_exercise_id)
    sample_row = {"foo": "bar", "spam": "eggs"}

    # When
    new_case_event_bytes = sample_loader.create_new_case_event(sample_row)

    # Then
    new_case_event = json.loads(new_case_event_bytes)

    # Check the header
    header = new_case_event['header']
    assert header['version'] == Config.EVENT_SCHEMA_VERSION
    assert header.get('dateTime')
    assert header.get('source')
    assert header.get('channel')
    assert header.get('messageId')
    assert header.get('correlationId')
    assert header.get('originatingUser')

    # Check the body
    new_case = new_case_event['newCase']
    assert new_case['collectionExerciseId'] == str(collection_exercise_id)
    assert new_case.get('caseId')
    assert new_case['sample'] == {'foo': 'bar'}
    assert new_case['sampleSensitive'] == {'spam': 'eggs'}

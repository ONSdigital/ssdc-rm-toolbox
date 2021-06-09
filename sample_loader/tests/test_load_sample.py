import csv
import json
from unittest import TestCase
from unittest.mock import patch
from sample_loader.load_sample import load_sample


@patch('sample_loader.load_sample.RabbitContext')
class TestLoadSample(TestCase):

    def test_load_sample_publishes_case_to_rabbit(self, patch_rabbit):
        sample_file = (
            'UPRN,ESTAB_UPRN,ADDRESS_LINE1,TOWN_NAME,POSTCODE',
            '10008677190,10008677191,Flat 56 Francombe House,Windleybury,XX1 0XX',
            '10008677191,10008677192,Flat 57 Francombe House,Windleybury,XX1 0XX')

        sample_units = load_sample(sample_file, 'test_ce_uuid', store_loaded_sample_units=True)

        self.assertEquals(len(sample_units), 2)

        patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value

        self.assertEqual(2, patch_rabbit_context.publish_message.call_count)
        publish_message_call_args = patch_rabbit_context.publish_message.call_args_list

        self._check_published_cases_contain_required_data(publish_message_call_args, sample_file)

    def test_load_sample_no_return_of_sample_units(self, patch_rabbit):
        sample_file = (
            'UPRN,ESTAB_UPRN,ADDRESS_LINE1,TOWN_NAME,POSTCODE',
            '10008677190,10008677191,Flat 56 Francombe House,Windleybury,XX1 0XX',
            '10008677191,10008677192,Flat 57 Francombe House,Windleybury,XX1 0XX')

        sample_units = load_sample(sample_file, 'test_ce_uuid', store_loaded_sample_units=False)

        self.assertEquals(len(sample_units), 0)

        patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value

        self.assertEqual(2, patch_rabbit_context.publish_message.call_count)
        publish_message_call_args = patch_rabbit_context.publish_message.call_args_list

        self._check_published_cases_contain_required_data(publish_message_call_args, sample_file)

    def _check_published_cases_contain_required_data(self, publish_message_call_args, sample_file):
        sample_file_rows = csv.DictReader(sample_file)
        for row_number, sample_row in enumerate(sample_file_rows):
            message_contents = json.loads(publish_message_call_args[row_number][0][0])
            self.assertEqual(sample_row['UPRN'], message_contents['sample']['UPRN'])
            self.assertEqual(sample_row['ADDRESS_LINE1'], message_contents['sample']['ADDRESS_LINE1'])

from toolbox.sample_loader.generate_sample import SampleGenerator
from toolbox.sample_loader.schema import SCHEMA
from toolbox.sample_loader.validate_sample import SampleValidator


def test_generated_sample_passes_validation(tmp_path):
    # Given
    generated_sample_path = tmp_path.joinpath('generated_sample.csv')

    # When
    SampleGenerator(SCHEMA).generate_sample_file(100, generated_sample_path)

    # Then
    validation_failures = SampleValidator().validate(generated_sample_path)
    assert not validation_failures, 'Should find no validation failures in generated sample'

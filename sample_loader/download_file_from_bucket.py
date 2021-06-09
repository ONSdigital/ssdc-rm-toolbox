import argparse
import os

from google.cloud import storage


def load_bucket_sample_file(sample_file):
    client = storage.Client()

    bucket = client.get_bucket(os.getenv('SAMPLE_BUCKET'))
    blob = storage.Blob(sample_file, bucket)

    with open(os.path.join("sample_files", sample_file), 'wb+') as file_obj:
        client.download_blob_to_file(blob, file_obj)

    print(f'downloaded file {sample_file} from gcp bucket {os.getenv("SAMPLE_BUCKET")}')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Download sample file from bucket')
    parser.add_argument('--sample_file',
                        required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    load_bucket_sample_file(args.sample_file)

import argparse
import glob
import os

from google.cloud import pubsub_v1

CHUNK_SIZE = 1


def dump_messages(project, topic, source):
    print("Publishing messages...", end="")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)

    os.chdir(source)
    for filename in glob.glob("*.json"):
        with open(filename, 'rb') as message_file:
            print(".", end="")
            future = publisher.publish(topic_path, data=message_file.read())
            future.result(timeout=30)

    print()
    print("Published all files")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Dump all files from a directory onto a Google Pub/Sub topic')
    parser.add_argument('topic', help='The topic to publish to', type=str)
    parser.add_argument('--project', help='The project the topic belongs to',
                        type=str, default='project')
    parser.add_argument('--source', help='The folder to publish files from',
                        type=str, default='.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    dump_messages(args.project, args.topic, args.source)

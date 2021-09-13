import argparse
import uuid

from google.api_core import retry
from google.cloud import pubsub_v1

CHUNK_SIZE = 1


def dump_messages(project, subscription, destination):
    print("Pulling messages...", end="")

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    with subscriber:
        while True:
            response = subscriber.pull(request={"subscription": subscription_path, "max_messages": CHUNK_SIZE,
                                                "return_immediately": True},
                                       retry=retry.Retry(deadline=1))

            if response.received_messages:
                print(".", end="")

                ack_ids = []
                for received_message in response.received_messages:
                    with open(f'{destination}/{uuid.uuid4()}.json', 'wb') as message_file:
                        message_file.write(received_message.message.data)
                        ack_ids.append(received_message.ack_id)

                subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})
            else:
                print()
                print("Subscription drained of all messages")
                break


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Dump all messages from a Google Pub/Sub subscription to files')
    parser.add_argument('subscription', help='The subscription to pull from', type=str)
    parser.add_argument('--project', help='The project the subscription belongs to',
                        type=str, default='project')
    parser.add_argument('--destination', help='The folder to dump files to',
                        type=str, default='.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    dump_messages(args.project, args.subscription, args.destination)

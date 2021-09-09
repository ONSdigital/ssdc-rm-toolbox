# SSDC RM Toolbox

The most bestestest tools for make running the social survey big success wow.

## How to use - Find and remove messages on pubsub

This tool will allow you to be able to find and delete messages on a pubsub topic
### Arguments

| Name                      | Description                                                                                                         |                                                                                        
| ---------------------     | ------------------------------------------------------------------------------------------------------------------- |
| `subscription name`       | Pubsub subscription name to look on                                                                                 |
| `subscription project id` | GCP project name                                                                                                    |
| `-s --search`             | Search for a string inside of the pubsub message body                                                               |                                                  
| `DELETE`                  | Used with `message_id`, deletes pubsub message of the id supplied                                                   |
| `message_id`              | Message id of the pubsub message                                                                                    |



View messages on pubsub subscription:
   ```bash
   python -m toolbox.message_tools.get_pubsub_messages <subscription name> <subscription project id>
   ```
   
View messages on a pubsub subscription with bigger limit:
   ```bash
   python -m toolbox.message_tools.get_pubsub_messages <subscription name> <subscription project id> -l <limit>
   ```
   
Search for a message:
   ```bash
   python -m toolbox.message_tools.get_pubsub_messages <subscription name> <subscription project id> -s <search term>
   ```

Delete message on pubsub subscription:   
   ```bash
   python -m toolbox.message_tools.get_pubsub_messages <subscription name> <subscription project id> <message_id> DELETE
   ```
   
   
## How to use - Moving messages from pubsub to bucket
Move messages from pubsub to a GCS bucket
### Arguments

| Name                      | Description                                                                                                         |                                                                                        
| ---------------------     | ------------------------------------------------------------------------------------------------------------------- |
| `subscription name`       | Subscription name to look on                                                                                        |
| `subscription project id` | GCP project name                                                                                                    |
| `bucket name`             | Bucket you want to move the pubsub message to                                                                       |                                                  
| `message_id`              | Message id of the pubsub message you want to move                                                                   |



Moving a pubsub message to a bucket:
```bash
python -m toolbox.message_tools.put_message_on_bucket <subscription name> <subscription project id> <bucket name> <message_id>
```
## How to use - publishing message from GCS bucket to pubsub topic

Publishing message from GCS bucket to pubsub topic
### Arguments

| Name                      | Description                                                                                                         |                                                                                        
| ---------------------     | ------------------------------------------------------------------------------------------------------------------- |
| `topic name`              | topic name to put message on                                                                                               |
| `project id`              | GCP project name                                                                                                    |
| `bucket name`             | Bucket you want to move the pubsub message to                                                                       |                                                  
| `bucket blob name`        | Name of the blob you want to publish to a topic                                                                     |                                                  

Publishing message from GCS bucket to pubsub topic:
```bash
python -m toolbox.message_tools.publish_message_from_bucket <topic name> <project id> <bucket blob name> <bucket name>
```

## QID Checksum Validator
A tool to check if a QID checksum is valid. Also shows the valid checksum digits if the QID fails. 

### Usage
```bash
qidcheck <QID>
```

### Arguments
| Name                      | Description                                                                                                         |                                                                                        
| ---------------------     | ------------------------------------------------------------------------------------------------------------------- |
| `qid`                     | The QID you wish to validate                                                                                        |

#### Optional Arguments
A non-default modulus and or factor for the checksum algorithm can be used with the optional flags `--modulus` and `--factor` 
   
## SFTP Support Login
To connect to SFTP (i.e. GoAnywhere) to check print files (read only). 

### Usage
```bash
doftp
```

## Uploading a file to a bucket
To upload a file to a bucket.

### Usage
```bash
uploadfiletobucket <file> <project> <bucket>
```

## Dumping all the messages on a Pub/Sub subscription to files
To dump all the messages queued up on a subscription

### Usage
```bash
dumpsubscriptiontofiles <subscription> [--project <project>] [--destination <destination folder>]
```

## Dumping all the message files in a directory to a Pub/Sub topic
To dump all the message files stored in a directory onto a topic

### Usage
```bash
dumpfilestotopic <topic> [--project <project>] [--source <source folder>]
```

## Running in Kubernetes
To run the toolbox in a kubernetes environment, you'll have to create the deployment using the YAML files in ssdc-rm-kubernetes. If you do not have a Cloud SQL Read Replica, use the dev deployment YAML file

Once the pod is up, you can connect to it:
```bash
kubectl exec -it $(kubectl get pods --selector=app=ssdc-rm-toolbox -o jsonpath='{.items[*].metadata.name}') -- /bin/bash
```

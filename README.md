# ssdc-rm-toolbox
test
# Census sample loader
This project contains a simplified sample loading script for Response Management case setup. (Currently in use for performance test setup on Kubernetes) It will take as arguments a sample CSV file, a Collection Exercise UUID

The Sample Loader will generate UUIDs for Sample Units and place messages directly onto the sample queue.
 Case service will then create corresponding Cases.
All of the attributes will be added to the queue as part of the message
  

## Setting up the python environment
This project uses pyenv and pipenv for python version and dependency management, install with
```shell script
brew install pyenv pipenv
```

Install dependencies with
```shell script
make build
```

Enter the environment shell with
```shell script
pipenv shell
```

## Building and pushing the docker container
```shell script
docker build -t eu.gcr.io/census-rm-ci/rm/ssdc-rm-toolbox:<TAG> .
docker push eu.gcr.io/census-rm-ci/rm/ssdc-rm-toolbox:<TAG>
```

## Testing Locally with Docker
To test the script locally you must run a RabbitMQ container. A docker-compose.yml file exists for this purpose.

```shell script
docker-compose up -d
```

Once RabbitMQ is running you can run the sample loader.


## Sample Loader
### Usage
```shell script
pipenv run python -m sample_loader.load_sample sample_loader/sample_file.csv 39616e56-40f6-4361-952a-cdf5bf193b94
```

### Logging
You can set the global log level with the `LOG_LEVEL` environment variable, when the sample loader runs as a script it defaults to `INFO` logging from script itself and `ERROR` for other log sources (e.g. pika).


### Viewing messages in the Rabbit queue
The Rabbit docker image included in docker-compose.yml has the management plugin enabled. This can be accessed when runnning on http://localhost:15672 use guest:guest as the credentials.


### Running in Kubernetes
To run the load_sample app in Kubernetes 

```shell script
./run_in_kubernetes.sh
```

You can also run it with a specific image rather than the default with
```shell script
IMAGE=fullimagelocation ./run_in_kubernetes.sh
```

This will deploy a sample loader pod in the context your kubectl is currently set to and attach to the shell, allowing you to run the sample loader within the cluster. The pod is deleted when the shell is exited.

### Copying across a sample file
To get a sample file into a pod in kubernetes you can use the `kubectl cp` command

While the sample loader pod is running, from another shell run
```shell script
kubectl cp <path_to_sample_file> <namespace>/<sample_load_pod_name>:<destination_path_on_pod>
```

### Downloading a sample file from bucket
Given a file is in the sample bucket, shell into the sample pod, then run command
```shell script
SAMPLE_BUCKET=<env_name>-sample python download_file_from_bucket.py --sample_file <name_of_file_in_bucket.csv>
```

This will download the file from the bucket onto the persistent volume which is mounted to the directory: /home/sampleloader/sample_files 



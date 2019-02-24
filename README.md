# smartthings_logging
Python module to log SmartThings data to CloudWatch

## Installing

### RedHat / AmazonLinux 2017

```
sudo yum install gcc git python36 python36-devel
python36 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
pip3 install -e .
```

### Debian / Ubuntu

```
sudo apt install build-essential git python3.6 python3.6-dev
python3.6 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
pip3 install -e .
```

## Setup

#### TODO: Detail the following:
  * setup KMS
  * setup S3 (also need to remove hard-coded bucket name)
  * Setup smartthings\_cli
    * SmartThings\_cli Groovy App
    * Generate OAuth file
  * encrypt and upload config to S3
  * Required AWS permissions

## Running locally

```
source env/bin/activate
smartthings_logger
```

## Build for Lambda

```
bin/mk_lambda.sh
```

#### In the `build/` directory
* `lambda_function_all.zip`: contains all code from `lambda/`
* `lambda_function_complete.zip`: contains all code from `lambda/`, `src/`, and all dependencies, and can be run/used as a single Lambda deploy package
* `lambda_layer_all.zip`: contains all code from `src/` and all dependenices and can be used as a Lambda layer that is used by a Lambda function.
* Files in `layers/` are the individual library bundles, suitable for use as layers for individual/specific libraries
* Files in `functions/` are packages for each module file from `lambda/`

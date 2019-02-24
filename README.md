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

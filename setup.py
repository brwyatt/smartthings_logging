#!/user/bin/env python

from setuptools import setup

setup(
    name='smartthings_logging',
    version='0.1.0',
    author='Bryan Wyatt',
    author_email='brwyatt@gmail.com',
    description=('Simple CLI to push data from SmartThings devices to '
                 'CloudWatch'),
    license='GPLv3',
    keywords='automation aws cli cloudwatch smartthings',
    url='https://github.com/brwyatt/smartthings_logging',
    packages=['smartthings_logging'],
    include_package_data=False,
    entry_points={
        'console_scipts': [
            'smartthings_log = smartthings_logging.cli:main'
        ],
    },
    install_requires=[
        'smartthings_cli',
        'boto3'
    ]
)

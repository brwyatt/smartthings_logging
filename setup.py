#!/user/bin/env python

from setuptools import setup, find_packages

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
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=False,
    entry_points={
        'console_scripts': [
            'smartthings_logger = smartthings_logging.cli:main'
        ],
    },
    install_requires=[
        'smartthings_cli',
        'boto3',
        'cryptography'
    ]
)

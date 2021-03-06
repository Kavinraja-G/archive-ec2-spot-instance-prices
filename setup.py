from setuptools import setup

setup(
    name='archivespotprices',
    version='0.0.1',
    description='Archive AWS EC2 Spotprices in Datasette',
    url='https://github.com/Kavinraja-G/archive-ec2-spot-instance-prices',
    author='Kavinraja G',
    author_email='rajakavin327@gmail.com',
    packages=['spotprices'],
    install_requires=['boto3', 'sqlite-utils', 'datasette']
)

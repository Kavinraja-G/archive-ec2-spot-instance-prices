Project Overview & Installation Guide
=====================================

Building a system to crawl the spot instance prices across regions for
all instance types from amazon APIs and archive them in a database and
also provide an API to access it.

Getting Started
---------------

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on how to deploy the project on a live system. Better to have
the repo cloned into the local directory.

Prerequisites
~~~~~~~~~~~~~

What things you need to install the software and how to install them

-  Python 3.6 or above
-  AWS Account with Credentials configured in ``.aws/credentials``
   folder or Export as environment variables
-  ``pip`` or higher

Installing
~~~~~~~~~~

A step by step series of examples that tell you how to get a development
env running

Use pip to install the required packages mentioned in the
``requirements.txt`` file

::

    pip3 install -r requirements.txt

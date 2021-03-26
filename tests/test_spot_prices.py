import boto3
from botocore.exceptions import EndpointConnectionError
from datetime import datetime

ec2_client = None

def test_get_ec2_client():
    global ec2_client
    ec2_client = boto3.client('ec2',region_name = 'us-east-1')
    assert ec2_client is not None

def test_spot_prices():
    global ec2_client
    spot_price_response = {}
    try:
        spot_price_response = ec2_client.describe_spot_price_history(
            InstanceTypes       = ['t3.medium'],
            ProductDescriptions = ['Linux/UNIX'],
            StartTime           = datetime.now(),
            EndTime             = datetime.now()
        )
    
    except EndpointConnectionError as _error:
        spot_price_response = {}
    finally:
        assert spot_price_response != {}
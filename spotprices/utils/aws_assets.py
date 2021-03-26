import boto3, json, logging
from os import path

# Logger Configuration
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s :: %(message)s')
logger = logging.getLogger(__name__)


# Get all ec2 instance types for a region
def get_all_instance_types(region):
    """
    Function to get all the instances types in a particular region

    Args:
        **region (str):** A valid AWS-region should be passed in this function as a argument  

    Returns:
        **List:** A list of all instance types in a particular region        

    Examples:
        >> *get_all_instance_types('us-east-1')* 
        
        *['t2.micro', 't2.medium', 'c5.xlarge',...]*

    """
    ec2 = boto3.client('ec2', region_name=region)
    responses = ec2.describe_instance_types()
    return [response['InstanceType'] for response in responses['InstanceTypes']]


# To get all the regions of the AWS Account
def get_all_regions():
    """
    Function to get all the regions in the AWS Account that is configure via the *.aws/credentials*

    Args:
        None  

    Returns:
        **List:** A list of all regions that are enabled in the AWS account.        

    Examples:
        >> *get_all_regions()* 
        
        *['us-east-1', 'us-east-2', 'ap-southeast-1',...]*

    """
    logger.info('Getting AWS Regions...')
    ec2 = boto3.client('ec2')
    return [ region['RegionName'] for region in ec2.describe_regions()['Regions'] ]
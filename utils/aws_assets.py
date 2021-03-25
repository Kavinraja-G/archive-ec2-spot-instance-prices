import boto3, json, logging
from os import path

# Constants
filename = 'regions-and-zones.json'

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


# To get all the AZs for the regions and return a dictionary
def get_all_zones(regions):
    """
    Function to get all the Availability zones in the Regions of an AWS Account that is configure 
    via the *.aws/credentials*

    Args:
        **regions (list):** A valid list of AWS-regions should be passed in this function as a argument    

    Returns:
        **Dict:** A dictionary of AWS regions as the *key* and the list of Availabilty zones as the *value*        

    Examples:
        >> *get_all_zones(regions)* 
        
        *{ "sa-east-1": ["sa-east-1a", ...], ... }*

    """
    logger.info('Getting Availability Zones for all Regions...')
    regions_and_zones = {}
    for region in regions:
        ec2 = boto3.client('ec2', region_name = region)
        az_response = ec2.describe_availability_zones()
        regions_and_zones[region] = [zones['ZoneName'] for zones in az_response['AvailabilityZones']]
    return regions_and_zones


# Driver Function
def main():
    logger.info('Gathering Assets for AWS')

    if not path.exists(filename):
        regions = get_all_regions()
        regions_and_zones = get_all_zones(regions)
        with open(filename, 'w') as f:
            json.dump(regions_and_zones, f, indent=2)
    else:
        logger.warning("Assets already Exists!")


if __name__ == "__main__":
    main()
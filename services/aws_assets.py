import boto3
import json
from os import path

# Constants
filename = 'regions-and-zones.json'


# Get all ec2 instance types for a region
def get_all_instance_types(region):
    ec2 = boto3.client('ec2', region_name=region)
    responses = ec2.describe_instance_types()
    return [response['InstanceType'] for response in responses['InstanceTypes']]


# To get all the regions of the AWS Account
def get_all_regions():
    print('Getting AWS Regions...')
    ec2 = boto3.client('ec2')
    return [ region['RegionName'] for region in ec2.describe_regions()['Regions'] ]


# To get all the AZs for the regions and return a dictionary
def get_all_zones(regions):
    print('Getting Availability Zones for all Regions...')
    regions_and_zones = {}
    for region in regions:
        ec2 = boto3.client('ec2', region_name = region)
        az_response = ec2.describe_availability_zones()
        regions_and_zones[region] = [zones['ZoneName'] for zones in az_response['AvailabilityZones']]
    return regions_and_zones


# Driver Function
def main():
    print('Gathering Assets for AWS...')

    if not path.exists(filename):
        regions = get_all_regions()
        regions_and_zones = get_all_zones(regions)
        with open(filename, 'w') as f:
            json.dump(regions_and_zones, f, indent=2)
    else:
        print("Assets already Exists!")


if __name__ == "__main__":
    main()
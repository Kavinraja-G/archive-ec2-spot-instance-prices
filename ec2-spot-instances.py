import boto3
from sqlite_utils import Database

# Constants
table_name = "spotprices"

# DB Connection
db = Database("spot_prices.db", recreate = True)


# Get all ec2 instance types for a region
def get_all_instance_types(region):
    ec2 = boto3.client('ec2', region_name=region)
    responses = ec2.describe_instance_types()
    return [response['InstanceType'] for response in responses['InstanceTypes']]


# Get and Store EC2 Spot Instance Prices in DB
def store_ec2_spot_prices(regions_and_zones):
    global db
    for region, zones in regions_and_zones.items():
        print('REGION: ', region)
        instance_types = ['t2.micro']

        for instance_type in instance_types:
            print('InstanceType: ', instance_type)
            ec2 = boto3.client('ec2',region_name = region)
            spot_price_response = ec2.describe_spot_price_history(
                InstanceTypes=[instance_type],
                ProductDescriptions=['Linux/UNIX'],
                MaxResults = len(zones)
            )

            for price in spot_price_response["SpotPriceHistory"]:
                # Insert the Spot prices of EC2 in DB 
                db[table_name].insert(
                    {
                        "Region": region,
                        "AZ": price["AvailabilityZone"],
                        "InstanceType": instance_type,
                        "Product": price["ProductDescription"],
                        "Price": price["SpotPrice"] 
                    }
                )


# To get all the regions of the AWS Account
def get_all_regions():
    print('Getting AWS Regions...')
    ec2 = boto3.client('ec2')
    return [ region['RegionName'] for region in ec2.describe_regions()['Regions'] ]


# To get all the AZs for the regions and return a dictionary
def get_all_zones(regions):
    print('Getting AWS AZs for Regions...')
    regions_and_zones = {}
    for region in regions:
        ec2 = boto3.client('ec2', region_name = region)
        az_response = ec2.describe_availability_zones()
        regions_and_zones[region] = [zones['ZoneName'] for zones in az_response['AvailabilityZones']]
    return regions_and_zones


# Driver Function
def main():
    regions = get_all_regions()
    regions_and_zones = get_all_zones(regions)
    store_ec2_spot_prices(regions_and_zones)


if __name__ == "__main__":
    main()
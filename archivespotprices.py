import boto3
import json
import logging
from datetime import datetime
from utils import db as Database
from utils import aws_assets
from botocore.exceptions import EndpointConnectionError


# Constants
filename             = 'regions-and-zones.json'
database_name        = "spotprices"
table_name           = "spotprices"
time_stamp           = datetime.utcnow()
product_descriptions = ['Linux/UNIX']


# Logger Configuration
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s :: %(message)s')
logger = logging.getLogger(__name__)


# Init Database
db = Database.DB( database_name = database_name, table_name = table_name )


# Get and Store EC2 Spot Instance Prices in DB
def store_ec2_spot_prices(regions_and_zones):
    """
    Function to crawl all the ec2-spot-instance prices of all instances across all AZs in regions and store in a Database
    that is already created during the DB initialization.

    Args:
        **regions_and_zones (dict):** This is loaded locally from the file regions_and_zones.json created by 
        the module aws_assets.py

    Returns:
        **None**

    Examples:
        >> *store_ec2_spot_prices({ "sa-east-1": ["sa-east-1a"] })*

    """
    global db
    for region, _zones in regions_and_zones.items():
        ec2 = boto3.client('ec2',region_name = region)
        logger.info(f'Getting Spot-prices in {region}')
        instance_types = aws_assets.get_all_instance_types(region)

        try:
            spot_price_response = ec2.describe_spot_price_history(
                InstanceTypes       = instance_types,
                ProductDescriptions = product_descriptions,
                StartTime           = time_stamp,
                EndTime             = time_stamp
            )
        except EndpointConnectionError as _error:
            logger.warning(f'Skipping {region} due to Network issue while calling the API')
            continue

        for price in spot_price_response["SpotPriceHistory"]:
            logger.info(f'Inserting Spot-Price of Instance: {price["InstanceType"]} in AZ: {price["AvailabilityZone"]}')
            data = {
                    "Region": region,
                    "AZ": price["AvailabilityZone"],
                    "InstanceType": price["InstanceType"],
                    "Product": price["ProductDescription"],
                    "Price": price["SpotPrice"],
                    "TimeStamp": time_stamp
                }
            db.insert_data(data)


# Driver Function
def main():
    """
    This main function calls all sub-functions and also the sub-modules in an ordered way to achieve the end goal
    of archiving the database with the spot prices of the ec2-instances across all availability zones in all regions.
        
        - **aws_assets.main =>** This module is called to check whether *regions-and-zones.json* file is present in the
          local directory and if not it creates that
        - **store_ec2_spot_prices(region_and_zones) =>** This function is called with the parameter *regions_and_zones* 
          loaded with the dictionary(key, val) in the *regions-and-zones.json* file
    
    Args:
        **None**

    Returns:
        **None**

    """
    aws_assets.main()
    
    regions_and_zones = {}

    with open(filename, 'r') as f:
        regions_and_zones = json.load(f)
    
    store_ec2_spot_prices(regions_and_zones)


if __name__ == "__main__":
    main()
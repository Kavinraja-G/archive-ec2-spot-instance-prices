import boto3
import json
import logging
from datetime import datetime
from utils import db as Database
from utils import aws_assets
from botocore.exceptions import EndpointConnectionError


# Constants
database_name        = "spotprices"
table_name           = "spotprices"
time_stamp           = datetime.utcnow()
product_descriptions = ['Linux/UNIX']


# Logger Configuration
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s :: %(message)s')
logger = logging.getLogger(__name__)


# Init Database
db = Database.DB( database_name = database_name, table_name = table_name )


# Insert Spot-Prices of Regions into Database
def store_ec2_spot_prices(region, spot_prices):
    global db
    for price in spot_prices:
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


# Get EC2 Spot Instance Prices across all regions
def get_ec2_spot_prices(regions):
    """
    Function to crawl all the ec2-spot-instance prices of all instances across all AZs in regions using the boto3 aws
    SDK

    Args:
        **regions (list):** List of regions enabled in the AWS account that is fetched from the aws_assets module

    Returns:
        **None**

    Examples:
        >> *get_ec2_spot_prices([ "sa-east-1" ])*

    """
    
    for region in regions:
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

        store_ec2_spot_prices(region, spot_price_response["SpotPriceHistory"])


# Driver Function
def main():
    """
    This main function calls all sub-functions and also the sub-modules in an ordered way to achieve the end goal
    of archiving the database with the spot prices of the ec2-instances across all availability zones in all regions.
        
        - **aws_assets.get_all_regions =>** This module is called to get all the regions of the AWS account
        - **get_ec2_spot_prices(regions) =>** This function is called with the parameter *regions* 
          loaded with the dictionary(key, val) in the *regions-and-zones.json* file
    
    Args:
        **None**

    Returns:
        **None**

    """
    
    regions = aws_assets.get_all_regions()
    
    get_ec2_spot_prices(regions)


if __name__ == "__main__":
    main()
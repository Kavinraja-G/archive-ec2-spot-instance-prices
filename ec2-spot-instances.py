import boto3, json
from datetime import datetime
from services import db as Connection
from services import aws_assets

# Constants
database_name        = "spotprices"
table_name           = "spotprices"
time_stamp           = datetime.utcnow()
product_descriptions = ['Linux/UNIX']

# DB Connection
db = Connection.DB( database_name = database_name, table_name = table_name )


# Get and Store EC2 Spot Instance Prices in DB
def store_ec2_spot_prices(regions_and_zones):
    global db
    for region, _zones in regions_and_zones.items():
        print('REGION: ', region)
        # instance_types = get_all_instance_types(region)

        ec2 = boto3.client('ec2',region_name = region)
        spot_price_response = ec2.describe_spot_price_history(
            InstanceTypes       = ["t2.micro"],
            ProductDescriptions = product_descriptions,
            StartTime           = time_stamp,
            EndTime             = time_stamp
        )

        for price in spot_price_response["SpotPriceHistory"]:
            print(price["AvailabilityZone"], price["InstanceType"])
            # Insert the Spot prices of EC2 in DB 
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
    aws_assets.main()
    
    regions_and_zones = {}

    with open('regions-and-zones.json', 'r') as f:
        regions_and_zones = json.load(f)
    
    store_ec2_spot_prices(regions_and_zones)


if __name__ == "__main__":
    main()
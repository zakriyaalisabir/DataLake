import os
from dotenv import load_dotenv, find_dotenv
from troposphere.s3 import (VersioningConfiguration,
                            AccelerateConfiguration, CorsConfiguration,
                            CorsRules)


BUCKET_NAME_SUFFIX = 'DataLakeMockProjectPreBetaRelease'
BUCKETS = [["LandingZone", "Raw"],
           ["WorkZone", "Partially Processed"],
           ["GoldZone", "Final Processed"]]

BUCKET_CORS_CONFIG = CorsConfiguration(CorsRules=[CorsRules(
    AllowedOrigins=["*"], AllowedMethods=["POST", "PUT", "HEAD", "GET"],
    AllowedHeaders=["*"],
)])

BUCKET_VERSIONING_CONFIG = VersioningConfiguration(Status="Enabled")
BUCKET_ACCELERATION_CONFIG = AccelerateConfiguration(
    AccelerationStatus="Enabled")

load_dotenv(find_dotenv())

print('---------------------------------------------')
print('Loading .env ....')
print('Using VIRTUAL_ENV = ', os.getenv('VIRTUAL_ENV'))
print('Successfully loaded .env')
print('---------------------------------------------')

import os
import sys
import logging
import urllib.request

import boto3

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(name)s) %(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

DEFAULT_HOSTED_ZONE_ID = os.getenv('ROUTE53_HOSTED_ZONE_ID', None)
DEFAULT_RECORD_DOMAIN_NAME = os.getenv('ROUTE53_RECORD_DOMAIN_NAME', None)
PUBLIC_IP_SERVICE_HOST = os.getenv('PUBLIC_IP_SERVICE_HOST', 'http://myip.dnsomatic.com')


def update_record_sets(hosted_zone_id=DEFAULT_HOSTED_ZONE_ID, record_domain_name=DEFAULT_RECORD_DOMAIN_NAME):
    assert hosted_zone_id
    assert record_domain_name

    public_ip = urllib.request.urlopen(PUBLIC_IP_SERVICE_HOST).read().decode('utf8')
    logger.debug(f'PUBLIC_IP: {public_ip}')
    if public_ip:
        route53 = boto3.client('route53')
        response = route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Comment': 'VPN IP Update',
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_domain_name,
                        'Type': 'A',
                        'TTL': 600,
                        'ResourceRecords': [{
                            'Value': public_ip
                        }]
                    }
                }]
            }
        )
        logger.debug('response: {response}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-z, --hosted-zone-id',
                        dest='hosted_zone_id',
                        help='AWS HOSTED ZONE ID')
    parser.add_argument('-d', '--record-domain-name',
                        dest='record_domain_name',
                        help='')


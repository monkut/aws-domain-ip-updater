import os
import sys
import logging
import urllib.request
from pathlib import Path

import boto3

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(name)s) %(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

DEFAULT_HOSTED_ZONE_ID = os.getenv('ROUTE53_HOSTED_ZONE_ID', None)
DEFAULT_DOMAIN_NAME = os.getenv('ROUTE53_DOMAIN_NAME', None)
PUBLIC_IP_SERVICE_HOST = os.getenv('PUBLIC_IP_SERVICE_HOST', 'http://myip.dnsomatic.com')


def update_record_sets(hosted_zone_id=DEFAULT_HOSTED_ZONE_ID, domain_name=DEFAULT_DOMAIN_NAME):
    assert hosted_zone_id
    assert domain_name

    public_ip = urllib.request.urlopen(PUBLIC_IP_SERVICE_HOST).read().decode('utf8')
    logger.info(f'PUBLIC_IP: {public_ip}')
    
    # get previous
    previous_ip = None
    previous_ip_filepath = Path.home() / '.previous_ip'
    if previous_ip_filepath.exists():
        with previous_ip_filepath.open('r', encoding='utf8') as f:
            previous_ip = f.read().strip()

    if public_ip and public_ip != previous_ip:
        route53 = boto3.client('route53')
        response = route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Comment': 'VPN IP Update',
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': 'A',
                        'TTL': 600,
                        'ResourceRecords': [{
                            'Value': public_ip
                        }]
                    }
                }]
            }
        )
        logger.debug(f'response: {response}')
    else:
        logger.warning(f'Domain({domain_name}) not updated, public_ip={public_ip}, previous_ip={previous_ip}!')
    
    # record public_ip as previous
    with previous_ip_filepath.open('w', encoding='utf8') as out_f:
        logger.debug(f'Writting previous_ip to: {str(previous_ip_filepath)}')
        out_f.write(public_ip)  


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-z', '--hosted-zone-id',
                        dest='hosted_zone_id',
                        default=DEFAULT_HOSTED_ZONE_ID,
                        help='AWS HOSTED ZONE ID')
    parser.add_argument('-d', '--domain-name',
                        dest='domain_name',
                        help='domain name to update')
    parser.add_argument('--verbose',
                         action='store_true',
                         default=False,
                         help='If given, DEBUG information will be shown')
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    update_record_sets(hosted_zone_id=args.hosted_zone_id, domain_name=args.domain_name)    




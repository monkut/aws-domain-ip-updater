AWS_PROFILE={PROFILE_FOR_DNS_USER} /usr/local/bin/python3.6 -m pipenv run python update_record_sets.py --hosted-zone-id {HOSTED_ZONE_ID} --domain-name {DOMAIN_TO_UPDATE} --verbose


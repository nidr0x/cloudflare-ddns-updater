# Cloudflare Dynamic DNS Updater

This script updates the A and AAAA records of a domain hosted in Cloudflare with the current public IP address. This is useful when you are using services like `external-dns`.

## Dependencies

- Python 3
- urllib.request
- CloudFlare

## Usage

1. Install the dependencies using `pip install -r requirements.txt`
2. Define `$CLOUDFLARE_API_KEY` and `$CLOUDFLARE_EMAIL` with your credentials
3. Run the script using `python cloudflare-ddns.py`

## Code explanation

The script performs the following steps:

1. Retrieve the current public IP address using `ident.me` for both IPv4 and IPv6.
2. Login to the Cloudflare account and retrieve the list of zones.
3. For each zone, retrieve the DNS records.
4. If the type of the record is `A` or `AAAA`, compare the current IP address with the IP address in the record.
5. If the IP addresses are different, update the record with the current IP address.

Note: in the given example I'm using `external-secrets` with [Doppler](https://www.doppler.com/) to manage the credentials.


import requests
import CloudFlare

def external_ips():
    ipv4_url = 'https://ipv4.icanhazip.com/'
    ipv6_url = 'https://ipv6.icanhazip.com/'
    try:
        external_ipv6 = requests.get(ipv6_url).text.strip()
    except requests.exceptions.RequestException as e:
        print(f'Warning: Failed to obtain IPv6 address - {e}')
        external_ipv6 = None

    try:
        external_ipv4 = requests.get(ipv4_url).text.strip()
    except requests.exceptions.RequestException as e:
        exit(f'{ipv4_url}: failed - {e}')

    print(f"Current IP addresses are IPv4 {external_ipv4} and IPv6 {external_ipv6}")
    return (external_ipv4, external_ipv6)

def main():
    (external_ipv4, external_ipv6) = external_ips()
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get()
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print("zone_id=%s zone_name=%s" % (zone_id, zone_name))

        try:
            dns_records = cf.zones.dns_records.get(zone_id)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones/dns_records.get %d %s - API call failed' % (e, e))

        for dns_record in dns_records:
            if dns_record['type'] == 'A':
                if dns_record['content'] == external_ipv4:
                    print(f"Record {dns_record['name']} already up-to-date")
                else:
                    try:
                        data = {
                            'name': dns_record['name'],
                            'type': 'A',
                            'content': external_ipv4,
                            'proxied': dns_record['proxied']
                        }
                        cf.zones.dns_records.put(zone_id, dns_record['id'], data=data)
                        print(f"Record {dns_record['name']} updated successfully!")
                    except CloudFlare.exceptions.CloudFlareAPIError as e:
                        print(f"Error updating record {dns_record['name']}: {e}")
                    print(f"UPDATED: {dns_record['name']} {dns_record['content']} -> {external_ipv4}")

            elif dns_record['type'] == 'AAAA':
                if dns_record['content'] == external_ipv6:
                    print(f"Record {dns_record['name']} already up-to-date")
                else:
                    try:
                        data = {
                            'name': dns_record['name'],
                            'type': 'AAAA',
                            'content': external_ipv6,
                            'proxied': dns_record['proxied']
                        }
                        cf.zones.dns_records.put(zone_id, dns_record['id'], data=data)
                        print(f"Record {dns_record['name']} updated successfully!")
                    except CloudFlare.exceptions.CloudFlareAPIError as e:
                        print(f"Error updating record {dns_record['name']}: {e}")
                    print(f"UPDATED: {dns_record['name']} {dns_record['content']} -> {external_ipv6}")

    exit(0)

if __name__ == '__main__':
    main()

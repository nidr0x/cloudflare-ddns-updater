import urllib.request
import CloudFlare

def external_ip():
    url = 'https://ident.me'
    try:
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    except:
        exit('%s: failed' % (url))
    if external_ip == '':
        exit('%s: failed' % (url))
    print(f"Current IP address is {external_ip}")
    return external_ip

def main():
    external_ip_address = external_ip()
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get()
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print("zone_id=%s zone_name=%s" % (zone_id, zone_name))

    zone = zones[0]
    zone_id = zone['id']

    try:
        dns_records = cf.zones.dns_records.get(zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records.get %d %s - API call failed' % (e, e))

    for dns_record in dns_records:
        r_name = dns_record['name']
        r_type = dns_record['type']
        r_value = dns_record['content']
        r_id = dns_record['id']
        r_proxied = dns_record['proxied']
        if r_type == 'A':
            if r_value == external_ip_address:
                print(f"Record {r_name} already up-to-date")
            else:
                try:
                    data = {
                        'name': r_name,
                        'type': r_type,
                        'content': external_ip_address,
                        'proxied': r_proxied 
                    }
                    cf.zones.dns_records.put(zone_id, r_id, data=data)
                    print(f"Record {r_name} updated successfully!")
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    print(f"Error updating record {r_name}: {e}")
                print('UPDATED: %s %s -> %s' % (r_name, r_value, external_ip_address))
    exit(0)

if __name__ == '__main__':
    main()

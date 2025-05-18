import os
import json

def filter_proxies():
    RAW_DIR = os.path.join(os.path.dirname(__file__), 'raw')
    ALL_JSON = os.path.join(RAW_DIR, 'all.json')
    proxies = []
    for fname in os.listdir(RAW_DIR):
        if not fname.endswith('.json') or fname == 'all.json':
            continue
        fpath = os.path.join(RAW_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                continue
        # proxify.json: list of dicts
        if fname == 'proxify.json' and isinstance(data, list):
            for entry in data:
                proxies.append({
                    'ip': entry.get('ip', ''),
                    'port': entry.get('port', ''),
                    'type': entry.get('protocol', ''),
                    'level': entry.get('anonymity', ''),
                    'country': entry.get('geolocation', {}).get('country', '')
                })
        # mtproto.json: list of dicts
        elif fname == 'mtproto.json' and isinstance(data, list):
            for entry in data:
                proxies.append({
                    'ip': entry.get('ip', ''),
                    'port': entry.get('port', ''),
                    'type': 'socks5',
                    'level': 'elite',
                    'country': entry.get('country', '')
                })
        # proxyscrape.json: dict with 'proxies' key
        elif fname == 'proxyscrape.json' and isinstance(data, dict):
            for entry in data.get('proxies', []):
                proxies.append({
                    'ip': entry.get('ip', ''),
                    'port': entry.get('port', ''),
                    'type': entry.get('protocol', ''),
                    'level': entry.get('anonymity', ''),
                    'country': entry.get('ip_data', {}).get('countryCode', '')
                })
    with open(ALL_JSON, 'w', encoding='utf-8') as f:
        json.dump(proxies, f, indent=2)

    print('status:success')

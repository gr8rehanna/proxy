import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

ALL_JSON = 'raw/all.json'
PROXY_JSON = 'proxy.json'
checkDomain = 'http://httpbin.org/ip'
#checkDomain = 'https://clients3.google.com/generate_204'

# Step 1: Remove duplicates by IP
def remove_duplicates():
    with open(ALL_JSON, 'r', encoding='utf-8') as f:
        proxies = json.load(f)
    seen = set()
    unique = []
    for p in proxies:
        if p['ip'] not in seen:
            seen.add(p['ip'])
            unique.append(p)
    removed = len(proxies) - len(unique)
    with open(ALL_JSON, 'w', encoding='utf-8') as f:
        json.dump(unique, f, indent=2)
    print(f"Loaded: {len(proxies)} Proxies\nRemoved {removed} Proxies as duplicate.\nUpdated all.json with {len(unique)} proxies.")
    return unique

def check_proxy(proxy, timeout=20):
    ip = proxy['ip']
    port = proxy['port']
    types = ['socks5', 'socks4'] if proxy['type'] == 'socks5' else ['socks4', 'socks5']
    for t in types:
        proxies_dict = {
            'http': f'{t}://{ip}:{port}',
            'https': f'{t}://{ip}:{port}'
        }
        try:
            start = time.time()
            resp = requests.get(checkDomain, proxies=proxies_dict, timeout=timeout)
            ms = int((time.time() - start) * 1000)
            if resp.status_code == 200:
                if t != proxy['type']:
                    return True, t, ms  # Fixed type
                return True, proxy['type'], ms
        except Exception:
            continue
    return False, proxy['type'], None

def process_batch(batch, batch_num, results):
    print(f"Running batch {batch_num} with {len(batch)} proxies.")
    success, failed, fixed = 0, 0, 0
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_proxy = {executor.submit(check_proxy, p): p for p in batch}
        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            ok, typ, ms = future.result()
            if ok:
                if typ != proxy['type']:
                    fixed += 1
                    proxy['type'] = typ
                proxy['ms'] = ms
                results.append(proxy)
                success += 1
            else:
                failed += 1
    print(f"Batch {batch_num} completed: Success: {success} | Failed: {failed} | Fixed type: {fixed}")
    with open(PROXY_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

def sort_proxies_by_country():
    try:
        with open(PROXY_JSON, 'r', encoding='utf-8') as f:
            proxies = json.load(f)
        proxies.sort(key=lambda x: x.get('country', ''))
        with open(PROXY_JSON, 'w', encoding='utf-8') as f:
            json.dump(proxies, f, indent=2)
        print(f"Sorted {len(proxies)} proxies.")
    except Exception as e:
        print(f"Sorting failed: {e}")

def main():
    proxies = remove_duplicates()
    print(f"Processing {len(proxies)} Proxies from all.json")
    batch_size = 10
    results = []
    for i in range(0, len(proxies), batch_size):
        batch = proxies[i:i+batch_size]
        process_batch(batch, i//batch_size+1, results)

def check_proxies():
    proxies = remove_duplicates()
    print(f"Processing {len(proxies)} Proxies from all.json")
    batch_size = 10
    results = []
    for i in range(0, len(proxies), batch_size):
        batch = proxies[i:i+batch_size]
        process_batch(batch, i//batch_size+1, results)
    sort_proxies_by_country()

if __name__ == '__main__':
    main()
    sort_proxies_by_country()

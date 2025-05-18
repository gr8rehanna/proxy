import requests


PROXIFY = 'https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.json'
PROXYSCRAP = 'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=socks4&proxy_format=ipport&format=json&timeout=20000'
MTPROTO = 'https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/socks.json' 
#MTPROTO = 'https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/socks.json'

## Using requests all files and save in json format with file name as provider in raw/$filename.json
def fetch_proxies():
    urls = {
        'proxify': PROXIFY,
        'proxyscrape': PROXYSCRAP,
        'mtproto': MTPROTO
    }
    
    for name, url in urls.items():
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            with open(f'raw/{name}.json', 'w') as file:
                file.write(response.text)
            print(f"Fetched {name} proxies successfully.")
        except requests.RequestException as e:
            print(f"Failed to fetch {name} proxies: {e}")

## RUN app in asynchronous way
if __name__ == "__main__":
    fetch_proxies()
    #fetch_proxies()
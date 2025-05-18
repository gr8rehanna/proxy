#!/usr/bin/env python3
"""
Simple script to fetch, filter, and check proxies, then exit.
"""
import time
import logging
from fetch import fetch_proxies
from filter import filter_proxies
from check import check_proxies

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_proxies():
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Update started {now}")
    fetch_proxies()
    filter_proxies()
    check_proxies()
    logging.info("Update complete. Goodbye!")

if __name__ == '__main__':
    update_proxies()
    print("Bye!")
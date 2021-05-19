#!/usr/bin/env python3

"""
APK Downloader
Author:     Jay Lux Ferro
Website:    https://sperixlabs.org
Date:       6th March, 2021
"""
from bs4 import BeautifulSoup as BS
import requests
import subprocess
import sys
import ssl
from os import path

base_url = 'https://apps.evozi.com/apk-downloader'
download_url = 'https://api-apk.evozi.com/download'

payload = {}

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'en-US,en;q=0.5',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': 'https://apps.evozi.com',
  'Connection': 'keep-alive',
  'Referer': 'https://apps.evozi.com/apk-downloader/'
}

def default_log():
    print('Process failed. Try again.')

def usage():
    print('Usage: {} [bundle identifier]\nE.g. {} com.ecgmobile'.format(path.basename(sys.argv[0]), path.basename(sys.argv[0])))
    sys.exit()


## entry
if len(sys.argv) != 2:
    usage()

bundle_identifier = sys.argv[1].strip()

## getting tokens from the website
print('[-] Processing...')
web_data = requests.get(base_url)
if web_data.status_code == 200:
    res = web_data.text.splitlines()
    token1 = res[195].strip().split(':')[1].strip().split(',')[0]
    token2 = res[164].strip().split('=')[-1].strip().replace("'", '').replace(';', '')
    token3 = res[195].strip().split('=')[-1].strip().replace(' ', '').strip('{').split(',')[:-1]

    payload[token3[0].split(':')[0]] = token1
    payload[token3[1].split(':')[0]] = bundle_identifier
    payload[token3[2].split(':')[0]] = token2
    payload['fetch'] = False

    res = requests.post(download_url, data=payload, headers=headers)
    try:
        res = res.json()
        if res['status'] == 'success':
            download_link = 'https:{}'.format(res['url'])
            print('PackageName: {}\nFileSize: {}\nHash(sha1): {}\nVersion: {}\nVersionCode: {}\nDownloadLink: {}\n'.format(res['packagename'], res['filesize'], res['sha1'], res['version'], res['version_code'], download_link))

            # trigger wget download file
            subprocess.call(['wget', download_link])
        elif res['status'] == 'error':
            print(res['data'])
        else:
            default_log()
    except:
        default_log()
else:
    default_log()
    if web_data.text.find('Cloudflare') != -1:
        print('Disable VPN or Proxy.')

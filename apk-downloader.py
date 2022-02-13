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
import re
from os import path, getenv
from cfproxy import CFProxy

base_url = "https://apksfull.com"
download_url = "{}/dl".format(base_url)
search_url = "{}/search/".format(base_url)
google_play_url = "https://play.google.com/store/apps/details?id={}"

payload = {}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "{}".format(base_url),
    "`Referer": "{}".format(search_url),
    "Connection": "keep-alive",
}


def default_log():
    print("Process failed. Try again.")
    sys.exit(1)


def usage():
    print(
        "Usage: {} [bundle identifier]\nE.g. {} com.ecgmobile".format(
            path.basename(sys.argv[0]), path.basename(sys.argv[0])
        )
    )
    sys.exit()


def download_file(data):
    global bundle_identifier
    print("[+] Downloading...")
    subprocess.call(
        ["wget", data["download_link"], "-O", "{}.apk".format(bundle_identifier)]
    )


def download_with_cf_work(url, data, headers):
    print("[+] Using Cloudflare Worker Proxy...")
    proxy = CFProxy(
        getenv("CF_IPROXY_HOST"), getenv("CF_USER_AGENT"), getenv("CF_DUMMY_IP")
    )
    res = proxy.post(url, data=data).json()
    if res["status"] == True:
        download_file(res)
    else:
        default_log()


## entry
if len(sys.argv) != 2:
    usage()

bundle_identifier = sys.argv[1].strip()

## getting tokens from the website
print("[-] Processing...")
res = requests.get(
    google_play_url.format(bundle_identifier), headers=headers, allow_redirects=True
)
if res.status_code != 200:
    default_log()

res = requests.get(
    "{}/{}".format(search_url, bundle_identifier), headers=headers, allow_redirects=True
)
if res.status_code != 200:
    default_log()

web_data = BS(res.content, "html.parser")
links = web_data.findAll("a")
dl_links = []

for link in links:
    _link = link.get("href")
    if _link.find("/download/") != -1:
        dl_links.append("{}{}".format(base_url, _link))

if len(dl_links) > 0:
    res = requests.get(dl_links[0], headers=headers, allow_redirects=True)
    if res.status_code != 200:
        default_log()

    web_data = BS(res.content, "html.parser").findAll("script")

    token = re.findall("token','([^']+)", web_data[-2].contents[0])[0]

    payload = {"token": token}
    res = requests.post(download_url, data=payload, headers=headers)
    if res.status_code != 200:
        default_log()

    data = res.json()
    if data["status"] == True:
        download_file(data)
    else:
        # checking  if cloudflare worker can be used
        if getenv("CF_TOKEN_VALUE") is not None:
            download_with_cf_work(download_url, payload, headers)
        else:
            print("[-] Process failed. Reason => {}".format(data["error"]))
else:
    default_log()

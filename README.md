### APK Downloader
- Python3
- Requires **wget** downloader

#### Instructions
1. Clone project
```
git clone https://github.com/jayluxferro/APK-Downloader
```

2. Install python dependencies using pip
```
cd APK-Downloader
pip install -r requirements.txt
```

#### Usage
```
python apk_downloader.py [bundle identifier]
```
Eg.
```
python apk_downloader.py com.ecgmobile
```

**NB**: To determine the bundle identifier, visit https://play.google.com/store/apps. Search for the app and the bundle identifier will show up in the URL; as shown below.<br/>
<img src='img/bundle_identifier.png' />

#### Limitations
**NB**: Might not work over a VPN or Proxy where some security checks are required before accessing web contents.

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
python apk-downloader.py [bundle identifier]
```
Eg.
```
python apk-downloader.py com.ecgmobile
```

**NB**: To determine the bundle identifier, visit https://play.google.com/store/apps. Search for the app and the bundle identifier will show up in the URL; as shown below.<br/>
<img src='img/bundle_identifier.png' />

#### Limitations
**NB**: Rate Limited. Try using a VPN.

#### Acknowledgement
1. https://github.com/EngineerDanny/apk-downloader

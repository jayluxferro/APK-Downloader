### APK Downloader
- Python3
- Requires **wget** downloader

#### Instructions
1. Clone project
```
git clone https://github.com/jayluxferro/APK-Downloader
cd APK-Downloader
```

2. Install python dependencies using pip
```
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

**NB**: To determine the bundle identifier, visit https://play.google.com/store/apps. Search for the app and the bundle identifier will show up in the url (as shown below).<br/>
<img src='img/bundle_identifier.png' />

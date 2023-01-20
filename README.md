# Final Fantasy XIV Retainer Item Checker

This script allows you to check for duplicate items on your Final Fantasy XIV character's retainers.

## Requirements
- Python 3.x
- requests
- bs4
- collections
- configparser

## Usage
1. Install the required packages by running `pip install -r requirements.txt`
2. Create a `config.ini` file in the same directory as the script and add your character ID and session cookie.
```
[DEFAULT]
CHARACTER_ID = 12345678
SESSION_COOKIE = ldst_sess=***
```
3. Run the script by executing `python script.py`
4. The script will print out any duplicate items found on your retainers.

## Note
- The script is scraping the data from the official Final Fantasy XIV Lodestone website, so the script may not work if the website is down or if the page structure is changed.
- The script uses a session cookie, so you will need to update the `SESSION_COOKIE` value in the `config.ini` file.
- The script reads the config file in the same directory, if you want to specify the full path of the config file please update the `config.read()` function in the script.

Please be aware that the use of this script could be against the terms of service of the official Final Fantasy XIV Lodestone website. Use it at your own risk.

Please don't forget to update the config.ini file with the correct values of your character id and session cookie as well as the full path of the config file if needed.
import os

# from Binance API
# visit: https://www.binance.com/en/my/settings/api-management

#API_KEY = "klk4CHcY4SeMMIl5xMUTGdIwDvQ5SpSTz0SHCjIhsxbpTAFH1mHykePHzgoWu5Cz"
#API_SECRET = "dsiP8UbPs9ZpqpHvBCbMHhZYaavU5A6qHnVhOmQBEqeIxSUIwmQH7pCYuFlIL8GR"

API_KEY = ""
API_SECRET = ""

API_CONFIG_FILE = "config.txt"

def isConfigExisted():
    if os.path.isfile(API_CONFIG_FILE):
        return True
    
    return False

def writeAPIConfig(key, passwd):
    global API_KEY, API_SECRET
    API_KEY = key
    API_SECRET = passwd

    with open(API_CONFIG_FILE, "w") as f:
        # API Key: XXXXXXXXXXXXXXX
        # API Secret: XXXXXXXXXXXX
        f.write("API Key: " + key)
        f.write("\n")
        f.write("Secret Key: " + passwd)

def getAPIConfig_dict():
    config_dict = {}
    with open(API_CONFIG_FILE, "r") as f:
        for line in f:
            (key, val) = line.split(':') # because of format setting in above
            config_dict[key] = val.replace(" ", "").replace("\n", "")
    
    return config_dict

def updateKeyAndSecret():
    global API_KEY, API_SECRET

    config = getAPIConfig_dict()
    API_KEY = config["API Key"]
    API_SECRET = config["Secret Key"]
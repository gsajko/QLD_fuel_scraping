# %%
import requests

import os
from datetime import datetime
import pandas as pd

# %%
# import json
# auth_path: str = "config/auth.json"
# auth = json.load(open(auth_path))
# TOKEN = auth["token"]
TOKEN = os.environ["TOKEN"]
fileList = os.listdir("data/")
week_of_year = datetime.now().strftime("%y_%V")

# %%
if f"{week_of_year}.csv" in fileList:
    df = pd.read_csv(f"data/{week_of_year}.csv")
else:
    columns = [
        "SiteId",
        "FuelId",
        "CollectionMethod",
        "TransactionDateUtc",
        "Price",
    ]
    df = pd.DataFrame(columns=columns)

# %%
url = "https://fppdirectapi-prod.fuelpricesqld.com.au/Price/GetSitesPrices?countryId=21&geoRegionLevel=3&geoRegionId=1"

payload = {}
headers = {
    "Authorization": f"FPDAPI SubscriberToken={TOKEN}",
    "Content-Type": "application/json",
}

response = requests.request("GET", url, headers=headers, data=payload)
if response.status_code == 200:
    print(response)
else:
    print(response)
    print(response.reason)
# %%
df_scraped = pd.DataFrame(response.json()["SitePrices"])
# check what month it is
# %%

# %%
df = df.append(df_scraped, sort=False)
# %%
df.drop_duplicates(inplace=True)
# %%
df.to_csv(f"data/{week_of_year}.csv", index=False)

# %%

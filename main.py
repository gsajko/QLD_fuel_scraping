# %%
import requests
import json
import os
from datetime import datetime
import pandas as pd

# %%
auth_path: str = "config/auth.json"
auth = json.load(open(auth_path))
fileList = os.listdir("data/")
current_month = datetime.now().strftime("%y_%m")
# %%
if f"{current_month}.csv" in fileList:
    df = pd.read_csv(f"data/{current_month}.csv")
else:
    columns = ['SiteId', 'FuelId', 'CollectionMethod', 'TransactionDateUtc', 'Price']
    df = pd.DataFrame(columns=columns)

# %%
url = "https://fppdirectapi-prod.fuelpricesqld.com.au/Price/GetSitesPrices?countryId=21&geoRegionLevel=3&geoRegionId=1"

payload = {}
headers = {
    "Authorization": f'FPDAPI SubscriberToken={auth["token"]}',
    "Content-Type": "application/json",
}

response = requests.request("GET", url, headers=headers, data=payload)
# %%
df_scraped = pd.DataFrame(response.json()["SitePrices"])
# check what month it is
# %%

# %%
df = df.append(df_scraped, sort=False)
# %%
df.drop_duplicates(inplace=True)
# %%
df.to_csv(f"data/{current_month}.csv", index=False)

# %%

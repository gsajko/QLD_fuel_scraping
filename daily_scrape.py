# %%
import os
from datetime import datetime

import pandas as pd
import requests

# %%
# import json
# auth_path: str = "config/auth.json"
# auth = json.load(open(auth_path))
# TOKEN = auth["token"]
TOKEN = os.environ["TOKEN"]
fileList = os.listdir("data/week/")
# %%
week_of_year_iso = datetime.now().isocalendar()
week_of_year = f"{week_of_year_iso[0]-2000}_{week_of_year_iso[1]}"
# make single digit weeks double digit by adding a 0
if len(week_of_year.split("_")[1]) == 1:
    week_of_year = f"{week_of_year_iso[0]-2000}_0{week_of_year_iso[1]}"

# %%
if f"{week_of_year}.csv" in fileList:
    df = pd.read_csv(f"data/week/{week_of_year}.csv")
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
url = (
    "https://fppdirectapi-prod.fuelpricesqld.com.au/"
    "Price/GetSitesPrices?countryId=21&geoRegionLevel=3&geoRegionId=1"
)

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

df = df.append(df_scraped, sort=False)
df.drop_duplicates(inplace=True)

df.to_csv(f"data/week/{week_of_year}.csv", index=False)

# %%

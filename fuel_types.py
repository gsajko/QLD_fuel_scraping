# %%

# %%
import json
import os

import requests

# auth_path: str = "config/auth.json"
# auth = json.load(open(auth_path))
# TOKEN = auth["token"]
TOKEN = os.environ["TOKEN"]
# %%


# %%
url_types = (
    "https://fppdirectapi-prod.fuelpricesqld.com.au/"
    "Subscriber/GetCountryFuelTypes?countryId=21"
)

payload = {}
headers = {
    "Authorization": f"FPDAPI SubscriberToken={TOKEN}",
    "Content-Type": "application/json",
}

response = requests.request("GET", url_types, headers=headers, data=payload)
if response.status_code == 200:
    print(response)
else:
    print(response)
    print(response.reason)
# %%
# save response to json file
with open("data/fuel_types.json", "w") as f:
    json.dump(response.json(), f)
# %%

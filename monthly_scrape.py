# %%
import requests
import json
import os
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

# %%
# url
url = "https://www.data.qld.gov.au/dataset/fuel-price-reporting"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")
# %% getting data from script into df
data = json.loads(soup.find("script", type="application/ld+json").string)
list_id = [i for i in data["@graph"]]
df = pd.DataFrame(list_id)
df = df[df["schema:encodingFormat"] == "CSV"]

# %% clean up df
columns_list = df.columns
columns_list = [col.replace("schema:", "") for col in columns_list]
df.columns = columns_list
df = df[["@id", "contentSize", "description", "encodingFormat", "name", "url"]]
df["@id"] = df["@id"].str.replace(
    "https://www.data.qld.gov.au/dataset/cb7a63ac-d6e1-4e78-9f9b-a23969ca052c/resource/",
    "",
    regex=True,
)

# %% scrape if needed
fileList = os.listdir("data/month")

for csv_url in df["url"]:
    name = csv_url.split("/")[-1]
    if name in fileList:
        pass
    else:
        print(f"downloading {name}")
        req = requests.get(csv_url)
        url_content = req.content
        csv_file = open(f"data/month/{name}", "wb")
        csv_file.write(url_content)
        csv_file.close()
# %%

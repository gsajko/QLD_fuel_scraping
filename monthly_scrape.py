# %%
import json
import os
import urllib.request
from datetime import datetime

import pandas as pd
import requests
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
df["date"] = df["name"].str.replace("Queensland Fuel Prices ", "")
df["date"] = pd.to_datetime(df.date.str.strip(), format="%B %Y").dt.to_period("M")
df.sort_values(by="date", inplace=True)
df.to_csv("data/monthly_list.csv", index=False)

# %% scrape if needed
fileList = os.listdir("data/month")
for index, row in df.iterrows():
    name = str(row.date) + "-" + row.url.split("/")[-1]
    if name in fileList:
        pass
    else:
        req = requests.get(row.url)
        print(f"downloading {name}")
        if req.status_code == 200:
            url_content = req.content
            csv_file = open(f"data/month/{name}", "wb")
            csv_file.write(url_content)
            csv_file.close()
        else:
            print(req.status_code)
            pass
# %%
# remove old weekly files if there is a new monthly file
last_scrape = str(df.iloc[-1, -1])
week_of_year_iso = datetime.strptime(last_scrape, "%Y-%m").isocalendar()
week_of_year = f"{week_of_year_iso[0]-2000}_{week_of_year_iso[1]}"
# %%
fileList = os.listdir("data/week/")
for file in fileList:
    nr = int(file.split(".")[0].replace("_", ""))
    week_nr = int(week_of_year.replace("_", ""))
    if nr < week_nr:
        os.remove(f"data/week/{file}")

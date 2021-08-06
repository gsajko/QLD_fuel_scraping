# QLD scrapping

Data is collected once a day.

 `'5 11 * * *'` Each day At 11:05

Scraped record are saved to a `.csv` file. Each week has a separate file in a format `[#year]_[#week].csv`.

For example we have 31th week of year 2021, file will be named `21_31.csv`.

You need to request for access token from https://www.fuelpricesqld.com.au/ ("Signing-up as a publisher or data consumer")

Each month data about fuel prices changes is published on: [Fuel Price Reporting](https://www.data.qld.gov.au/dataset/fuel-price-reporting).

This scrape is intentend to fill the gap after the last published month (I assume less then 2 months of time).

If you want to work on historic data older then 2 months, it's better to use Fuel Price Reporting.


# QLD scrapping

Data is collected once a day.

 `'11 * * * *'` Each hour at 11
 
Scraped records are saved to a `.csv` file. Each week has a separate file in the format `[#`year]_[#week].csv`.

For example, we have the 31st week of the year 2021, the file will be named `21_31.csv`.

You need to request for access token from https://www.fuelpricesqld.com.au/ ("Signing-up as a publisher or data consumer")

Each month data about fuel price changes are published on: [Fuel Price Reporting](https://www.data.qld.gov.au/dataset/fuel-price-reporting).

This scrape was made to fill the gap after the last published month (I assume less than 2 months).

If you want to work on historic data older than 2 months, it's better to use Fuel Price Reporting.


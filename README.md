# V-APP

## This simple script scrapes VLR.gg data and stores it in a MySQL database.
Required pip installs: Scrapy and MySQL

## Setup
```bash
scrapy startproject project_name
```

Copy the valorantspider.py file and enter a url from the VLR.gg 'Stats' webpage. You can select any filters, but the url must ultimately come from this page, since the script only scrapes this layout.
Set up your MySQL database settings in the settings.py file located one directory above the directory your spider file is in. If you don't wish to use a SQL database, you can comment out these lines using then run the option "-o filename.csv" to export as CSV.

## To run your spider, run the command:
```bash
scrapy crawl VCT
```

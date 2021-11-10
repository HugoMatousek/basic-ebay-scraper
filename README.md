# basic-ebay-scraper
A very basic ebay webscraper - done as [HW in CSCI40 at Claremont McKenna College](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03).

The scraper looks up the phrase on ebay and then gets the details about each offer from their individual pages.

The user can choose the search phrase, number of desired results, output file type (json default, csv available).

The outcome in the json/csv files lists all the products together with their: name, price (in cents), shipping cost (in cents), condition, boolean for free returns, and number of items already sold.

To use this scraper, run:
```$ python3 ebay-dl.py 'search term'``` 
where `'search term'` is the desired product you want to search

You can also add the following flags:
```--num=X
``` 
where `X` is the number of results you would like to get (default is 10)
``` 
--csv
``` 
which generates a `.csv` file instead of `.json`   

Commands used to generate the files in this repo:
```
$ python3 ebay-dl.py 'xperia 1 iii' --num=25
$ python3 ebay-dl.py 'hp spectre x360' --num=10 #technically not required as num=10 is the default value
$ python3 ebay-dl.py 'arduino uno' --num=12
$ python3 ebay-dl.py 'xperia 1 iii' --num=25 --csv
$ python3 ebay-dl.py 'hp spectre x360' --num=10 --csv #technically not required as num=10 is the default value
$ python3 ebay-dl.py 'arduino uno' --num=12 --csv
```

TO-DO:
- There are essentially no comments for the most of the time
- Efficiency is terrible
- Output the link, bid/sale/best-offer type

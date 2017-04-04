# London Areas' Indices

The aim of this project is to calculate the Foodie Index and the Mortgage Index of each of the 8 London Areas (East Central, West Central, Eastern, Western, South Eastern, South Western, North Eastern, North Western.

## Mortgage Index
In order to calculate the Mortgage Index we needed to acquire data from the Council of Mortgage Lenders

### Create Database
In order to find the Mortgage we receive the information from the Lending.xlsx that we acquired through the Council of Morgage Lenders. We then created a database where we would store that info.

### Calculating Mortgage Index
We decided to calculate the Mortgage Index of each area but testig each area's stationarity. By acquiring the info that we stored in our database and by simple data manipulation we created time series for each area.

## Foodie Index
In order to calculate the Foodie Index we needed to acquire data from Yelp

### Create Database
The Yelp Api is very limiting only allowing a specific amount of requests every day and returning 20 results per call and up to 1000 results per category. That meant that we had to use every possible category that had results for London in order to retrieve the majority of data info. Unfortunately there were some missed info that we have to ignore for the time being.

### Calculating the Foodie Index
We decided to calculate the Foodie Index of each area based on the density and the average rating. By doing so we acquired a specific index for each area. We plotted this by using Basemap and the London Areas.

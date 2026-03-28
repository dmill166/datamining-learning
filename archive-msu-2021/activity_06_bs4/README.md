# Activity 06

## Write a Simple Web Scraper

## Goal
The goal of this activity is have you write a simple web scraper using Beautiful Soup, saving the extracted information in JSON format. 
 
## Instructions

Because pages are structured differently, every scraper is unique.  Open [https://covidcheckcolorado.org/find-our-sites-testing](https://covidcheckcolorado.org/find-our-sites-testing/) and use your browser code inspection tools to strategize your scraper. Your scrape should produce the following JSON file:

```
{
    "name": "16th Street Mall", 
    "saliva_testing": true, 
    "address": "1600 California St", 
    "city": "Denver", 
    "state": "CO", 
    "zipcode": "80202", 
    "hours_of_operation": "Monday \u2013 Friday, 12pm \u2013 6:30pm"
}, 
{   "name": "All City Stadium", 
    "address": "1495 S. Race Street", 
    "city": "Denver", 
    "state": "CO", 
    "zipcode": "80210", 
    "hours_of_operation": "Monday \u2013 Wednesday, 7am \u2013 5pm; Thursday \u2013 Friday, 7am \u2013 1pm"
},
{   "name": "Littleton Park and Walk", 
    "indoor_testing": true, 
    "address": "190 East Littleton Blvd.", 
    "city": "Littleton", 
    "state": "CO", 
    "zipcode": "80120", 
    "hours_of_operation": "Monday \u2013 Friday: 7am \u2013 12pm"
}, 
...
```

Note that "16th Street Mall" provides "saliva testing", "All City Stadium" does NOT provide "saliva testing", and "Littleton Park and Walk" provides "indoor testing". That information needs to be extracted from the page and saved in a structured way. Hint: use regular expressions. 
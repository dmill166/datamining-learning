# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: A Simple Puppeteer Web Scraper

import asyncio
import pyppeteer
import os.path 
import json

URL = 'https://www.indeed.com/'
CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
DATA_PATH = '../data'
JSON_FILE = 'jobs.json'

async def main():

    # TODO: launch browser


    # TODO: open target URL

    # TODO: fill-in the "What" input field (e.g., Data Analyst)

    # TODO: click on the submit button
    
    await page.waitForNavigation( waitUntil = 'load' )

    # TODO: extract the name of the companies and their job positions url (if avaialable)
    

    # close the browser
    await browser.close()

    # export to json 
    with open(os.path.join(DATA_PATH, JSON_FILE), 'wt') as json_file:
        json.dump(jobs, json_file)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

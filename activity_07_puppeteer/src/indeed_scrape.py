# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: A Simple Puppeteer Web Scraper

import asyncio
from json.encoder import JSONEncoder
import pyppeteer
import os.path 
import json


original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
JSON_FILE = 'jobs.json'
JSON_PATH = os.path.join(DATA_FOLDER, JSON_FILE)
URL = 'https://www.indeed.com/'
CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

async def main():

    # TODO: launch browser
    browser = await pyppeteer.launch(
      headless = False,
      executablePath = CHROME_PATH
   )

    # TODO: open target URL
    page = await browser.newPage()
    await page.goto(URL, waitUntil = 'networkidle0')

    # TODO: fill-in the "What" input field (e.g., Data Analyst)
    await page.type('[@id="text-input-what"]', 'Data Analyst')
    #//*[@id="text-input-what"]
    #/html/body/div/div[2]/span/div[3]/div[1]/div/div/div/form/div[1]/div[1]/div/div[2]/input

    # TODO: click on the submit button
    await page.click('[@id="whatWhereFormId"]')
    # //*[@id="whatWhereFormId"]/div[3]/button
    await pyppeteer.page.waitForNavigation( waitUntil = 'load' )

    # TODO: extract the name of the companies and their job positions url (if avaialable)
    

    # close the browser
    await pyppeteer.browser.close()

    # export to json 
    with open(JSON_PATH, 'wt') as json_file:
        json.dump(pyppeteer.jobs, json_file)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

import json
import asyncio
import pyppeteer
import os
import csv
import re
import time

# definitions/parameters
DATA_FOLDER    = os.path.join('..', 'data')
OUTPUT_FILE_NAME = 'smartphones.json'
CHROME_PATH    = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
URL            = 'https://www.productchart.com/smartphones/'

async def main():

    # launch browser
    browser = await pyppeteer.launch(
        headless = False,
        executablePath = CHROME_PATH
    )

    # open target URL
    page = await browser.newPage()
    await page.goto(URL, waitUntil = 'networkidle0')

    # extract info
    items = await page.xpath("//a[@class='item']")
    print(len(items), end=', ')

    # get all the links first
    links = []
    for item in items:

        # get the link 
        link = await page.evaluate(
            '(element) => element.href', 
            item
        )
        links.append(link) 
    await page.close()
    
    # get the specs
    smartphones = []
    count = 0
    for link in links:
        count += 1
        # if count > 5:
        #     break
        page = await browser.newPage()
        await page.goto(link, waitUntil = 'networkidle0')

        # name and price
        target = await page.xpath("//td[@class='name']")
        handle = await target[0].getProperty('textContent')
        text = await handle.jsonValue()
        text = text.replace('\n', ' ').strip()
        name = text.split('$')[0]
        name = name.replace('For ', '').strip()
        match = re.search('For (\$.+) on', text)
        print(name, end=',')
        if match:
            price = match.group(1)
            print(price, end=',')
        else:
            continue
        
        tds = await page.xpath("//td[@class='data']")
        smartphone = { 'name': name, 'price': price }
        i = 0
        headers = ['screen_size', 'screen_resolution', 'storage', 'ram', 'cpu', 'weight', 'dual_sim', 'sd-card', 'rear_camera', 'front_camera', 'battery', 'removable_battery', 'fingerprint_sensor', 'display_cutout', 'os', 'release_date']
        for td in tds:
            handle = await td.getProperty('textContent')
            value = await handle.jsonValue()
            smartphone[headers[i]]= value
            i += 1
        
        smartphones.append(smartphone)
        await page.close()

    print('done!')
    print(smartphones)
    # close the browser
    await browser.close()

    # update json
    with open(os.path.join(DATA_FOLDER, OUTPUT_FILE_NAME), 'wt') as json_file:
      json.dump(smartphones, json_file)

if __name__ == "__main__":
   asyncio.get_event_loop().run_until_complete(main())
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from time import sleep

from numpy import result_type

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}
weburl = 'https://www.amazon.com'
search_query = 'curtains'.replace(' ', '+')
base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)

items = []
for i in range(1,3):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = soup.find_all(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    print(len(urls))
    for result in urls:
        link_url = urljoin(weburl, result.get('href'))
        #print(link_url)
        page1 = requests.get(link_url, headers=headers)
        soup1 = BeautifulSoup(page1.content, "html.parser")
        title = soup1.find(class_='a-size-large product-title-word-break').text
        price = soup1.find('span', class_='a-offscreen').text
        description = soup1.find('div', id='feature-bullets').find(['ul', 'li', 'span']).text

        image_text = []
        brand =[]
        model =[]
        image = soup1.find_all(['img'])
        for j in image:
            image_url = j.get('src')
            if image_url is not None and '.jpg' in image_url:
                image_text = image_url

            prodDetails = soup1.find('div', id='prodDetails').find_all('tr')
            for row in prodDetails:
                th = row.find('th').text.strip()
                td = row.find('td').text.strip()
                if th == 'Brand':
                    brand = td
                if th == 'ASIN':
                    model = td

        items.append([title, price, description, image_text, brand, model])
df = pd.DataFrame(items, columns=['name', 'price', 'description', 'image url', 'brand', 'model'])
df.to_excel('p1.xlsx', index=False)

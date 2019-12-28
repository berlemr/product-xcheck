from datetime import datetime as dt
from datetime import timedelta

import requests
from bs4 import BeautifulSoup

from app.utils.mongo_handler import MongoHandler
from config import Config

URLS = {
        'OUTDOORS':"https://www.amazon.co.uk/Best-Sellers-Home-Garden/zgbs/home-garden/outdoors/",
        'BATH_OILS':'https://www.amazon.co.uk/Best-Sellers-Beauty-Bath-Oils/zgbs/beauty/',
        'HEALTH':"https://www.amazon.co.uk/Best-Sellers-Health-Personal-Care-Dietary-Management/zgbs/drugstore/"
    }

class AmzHandler(object):

    def __init__(self, name, url, cob = dt.now().date().strftime('%Y-%m-%d')):
        self.cob = cob
        self.name = name
        self.url = url

    def retrieve_url(self):
        r = requests.get(self.url)
        if r.status_code == 200: #success
            m = MongoHandler(Config.MONGODB,self.name)#add content to mongo
            data = {'start_date':self.cob, 'end_date':self.cob, 'html':r.content}
            m.insertIntoMongo(data)

    def getBestSellers(self,start_cob = (dt.now().date() - timedelta(5)).strftime('%Y-%m-%d')):
        d = {}
        m = MongoHandler(Config.MONGODB,self.name)
        data = m.getFromMongoByDateRange(start_cob,self.cob)
        for cob,content in data.items():
            soup = BeautifulSoup(content, 'html.parser')
            bestsellers = soup.find_all(class_= 'zg-item-immersion')#get each item
            d[cob] = bestsellers
        return d

    def processBestSellers(self,bestsellers):
        for cob,bestsellers in bestsellers.items():
            for item in bestsellers:
                try:
                    rank = int(item.find('span',class_='zg-badge-text').text.replace('#',''))
                    name = item.find('div',class_='p13n-sc-truncate p13n-sc-line-clamp-2').text
                    price = item.find(class_='p13n-sc-price').text.replace('£',''); price = float(price.split(' ')[0]) #lowest price
                    image = item.find('img')['src']
                    link = 'https://www.amazon.co.uk/' + item.find('a',class_='a-link-normal')['href']
                    print(f'{cob}|{rank}|{name}|{price}|{link}|{image}')
                except Exception as e:
                    print(e)

def main():
    # for k,v in URLS.items():
    #     a = AmzHandler(k,v)
    #     # a.retrieve_url()
    #     bestsellers = a.getBestSellers()
    #     a.processBestSellers(bestsellers)
    a = AmzHandler('OUTDOORS',URLS['OUTDOORS'])
    bestsellers = a.getBestSellers()
    a.processBestSellers(bestsellers)

if __name__=="__main__":
    main()
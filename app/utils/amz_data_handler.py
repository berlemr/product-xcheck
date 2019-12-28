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
        d = {}
        l = []
        for cob,bestsellers in bestsellers.items():
            for item in bestsellers:
                try:
                    rank = int(item.find('span',class_='zg-badge-text').text.replace('#',''))
                    item_name = item.find('div',class_='p13n-sc-truncate p13n-sc-line-clamp-2').text.lstrip().rstrip()
                    price = item.find(class_='p13n-sc-price').text.replace('£',''); price = float(price.split(' ')[0]) #lowest price
                    image = item.find('img')['src']
                    link = 'https://www.amazon.co.uk/' + item.find('a',class_='a-link-normal')['href']
                    if d.__contains__(item_name):
                        d[item_name]['data'].append((cob,rank,price))
                    else:
                        d[item_name] = {'link':link,'image':image,'data':[(cob,rank,price)]}
                    # print(f'{cob}|{rank}|{item_name}|{price}|{link}|{image}')
                except Exception as e:
                    print(e)
                finally:
                    if cob == self.cob:
                        d[item_name]['name'],d[item_name]['current_rank'],d[item_name]['current_price'] = item_name,rank,price
                        l.append(d[item_name]) #should only include list of items that are in current best seller list
        return l

def main():
    # for k,v in URLS.items():
    #     a = AmzHandler(k,v)
    #     a.retrieve_url()

    a = AmzHandler('OUTDOORS',URLS['OUTDOORS'])
    bestsellers = a.getBestSellers()
    a.processBestSellers(bestsellers)

if __name__=="__main__":
    main()
import pandas as pd
import requests
from math import ceil
from bs4 import BeautifulSoup
import random
from re import sub

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0'
}
baseurl = "https://www.proshop.pl"

class category:
    def __init__(self, soup, parentName, numberOfCategory) -> None:
        self.aTag = soup.find('a')
        self.link = f"{baseurl}{self.aTag['href']}"
        self.categoryName = self.aTag.text
        self.parentName = parentName
        #Category number for creating image paths
        self.numberOfCategory = numberOfCategory
        #Product number for creating image paths
        self.numberOfProducts = 0
    
    def toDict(self):
        return {
            'Name': self.categoryName,
            'Parent category': self.parentName
        }
    
class product:
    def __init__(self, soup, categoryName, imgname) -> None:
        self.valid = True
        self.imgname = imgname
        self.categoryName = categoryName
        self.name = soup.find('h1').text.replace('>', '')
        #Standard
        try:
            self.price = soup.find('span', class_='site-currency-attention').text
        #Sale
        except:
            if(soup.find('div', class_='site-currency-attention site-currency-campaign') is not None):
                self.price = soup.find('div', class_='site-currency-attention site-currency-campaign').text
            else:
                self.price = soup.find('div', class_='site-currency-attention').text
       
        self.price = float(self.price.replace(' zł', '').replace(',', '.').replace('\xa0', ''))
        self.priceNetto = float(soup.find('span', class_='site-currency-sm').text.replace(' zł netto', '').replace(',', '.').replace('\xa0', ''))
        self.description = soup.find('p', class_='site-product-short-description').text
        self.quantity = random.randint(1,10)

        if random.uniform(0,1) > 0.05:
            self.availableForOrder = 1
        else :
            self.availableForOrder = 0

        mainImg = soup.find('div', class_='col-xs-12 text-center').find('a')['href']
        urls = []

        response = requests.get(f"{baseurl}{mainImg}", headers=headers)
        if response.status_code == 200:
            with open(f"./imgtoimport/{self.imgname}_{len(urls)}.jpg", 'wb') as plik:
                plik.write(response.content)
            urls.append(f"/var/www/html/imgtoimport/{self.imgname}_{len(urls)}.jpg")

        imgs = soup.find_all('div', class_='col-xs-3 col-sm-4 col-md-3 mt-1')

        for image in imgs:
            response = requests.get(f"{baseurl}{image.find('a')['href']}", headers=headers)
            if response.status_code == 200:
                with open(f"./imgtoimport/{self.imgname}_{len(urls)}.jpg", 'wb') as plik:
                    plik.write(response.content)
                urls.append(f"/var/www/html/imgtoimport/{self.imgname}_{len(urls)}.jpg")

            if len(urls)>1:
                break
        self.images = ';'.join(urls)
        #No images
        if len(urls)==0:
            self.valid = False


    
    def toDict(self):
        return {
            'Name': self.name,
            'Categories': self.categoryName,
            'Price tax excluded': self.priceNetto,
            'Price tax included': self.price,
            'Description': self.description,
            'Image URLs': self.images,
            'Quantity': self.quantity,
            'Available for order': self.availableForOrder

        }
    
class scraper:
    def __init__(self) -> None:
        self.mainCategories:list[category] = []
        self.subCategories:list[category] = []
        self.products:list[dict] = []
        self.numberOfCategories = 0

    def scrapeMainCategories(self):
        r = requests.get(baseurl, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        mainCategories = soup.find_all('li', class_='ps-nav__cat')
        for cat in mainCategories[2:6]:
            self.mainCategories.append(category(cat, 'Strona główna', self.numberOfCategories))
            self.numberOfCategories += 1
    
    def scrapeSubCategories(self):
        for cat in self.mainCategories:
            r = requests.get(cat.link, headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')
            subCategories = soup.find_all('li', class_='d-flex')
            for subCat in subCategories[:30]:
                self.subCategories.append(category(subCat,cat.categoryName, self.numberOfCategories))
                self.numberOfCategories += 1

    def deleteEmptyCategories(self):
        for cat in self.subCategories:
            if cat.numberOfProducts == 0:
                self.subCategories.remove(cat)

    def exportCategoriesToCsv(self):
        categories = []
        for cat in self.mainCategories:
            categories.append(cat.toDict())
        for cat in self.subCategories:
            categories .append(cat.toDict())
        dataFrame = pd.DataFrame(categories)
        dataFrame.to_csv('./results/categories.csv', sep='>', encoding='utf-8')

    def searchPages(self, cat:category, numOfPages):
        for i in range(numOfPages):
            r = requests.get(f"{cat.link}?pre=0&pn={i}", headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')
            productLinks = soup.find_all('a', class_='site-product-link')
            for prod in productLinks:
                r = requests.get(f"{baseurl}{prod['href']}", headers=headers)
                soup = BeautifulSoup(r.content, 'lxml')
                cat.numberOfProducts += 1
                p = product(soup, cat.categoryName, f"{cat.numberOfCategory}{cat.numberOfProducts}")
                if p.valid:
                    self.products.append(p.toDict())

    def scrapeProducts(self):
        for cat in self.subCategories:
            r = requests.get(f"{cat.link}?pre=0", headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')
            size = int(soup.find('div', class_='site-active-results-container').text.replace('Produkty w Twoim wyszukiwaniu: ',''))
            numOfPages = ceil(size/25)%2
            self.searchPages(cat, numOfPages)
        dataFrame = pd.DataFrame(self.products)
        dataFrame.to_csv('./results/products.csv', sep='>', encoding='utf-8')
    
    def scrape(self):
        self.scrapeMainCategories()
        self.scrapeSubCategories()
        self.scrapeProducts()
        self.deleteEmptyCategories()
        self.exportCategoriesToCsv()

s = scraper()
s.scrape()
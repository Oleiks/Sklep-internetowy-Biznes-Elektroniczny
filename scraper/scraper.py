import pandas as pd
import requests
from math import ceil
from bs4 import BeautifulSoup
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0'
}
baseurl = "https://www.proshop.pl"

class category:
    def __init__(self, soup, parentName, numberOfCategory) -> None:
        self.aTag = soup.find('a')
        self.link = f"{baseurl}{self.aTag['href']}"
        self.categoryName = self.aTag.text
        try:
            r = requests.get(self.link, headers=headers)
            s = BeautifulSoup(r.content, 'lxml')
            self.description = s.find('div', class_="site-fadeout-container").find('p').text
        except:
            self.description = self.categoryName
        self.parentName = parentName
        #Category number for creating image paths
        self.numberOfCategory = numberOfCategory
        #Product number for creating image paths
        self.numberOfProducts = 0
    
    def toDict(self):
        return {
            'Name': self.categoryName,
            'Parent category': self.parentName,
            'Description': self.description
        }
    
class product:
    def __init__(self, soup, categoryName, imgname) -> None:
        self.valid = True
        self.imgname = imgname
        self.categoryName = categoryName
        self.name = soup.find('h1').text.replace('>', '')[:128]
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
            with open(f"../results/images/{self.imgname}_{len(urls)}.jpg", 'wb') as plik:
                plik.write(response.content)
            urls.append(f"/var/www/html/images/{self.imgname}_{len(urls)}.jpg")

        imgs = soup.find_all('div', class_='col-xs-3 col-sm-4 col-md-3 mt-1')

        for image in imgs:
            response = requests.get(f"{baseurl}{image.find('a')['href']}", headers=headers)
            if response.status_code == 200:
                with open(f"../results/images/{self.imgname}_{len(urls)}.jpg", 'wb') as plik:
                    plik.write(response.content)
                urls.append(f"/var/www/html/images/{self.imgname}_{len(urls)}.jpg")

            if len(urls)>1:
                break
        self.images = ';'.join(urls)

        features = {'Szerokość':0.0,'Waga': 0.0, 'Wysokość':0.0, 'Głębokość':0.0}
        specifications = soup.find('div', id='specItemsAccordion')
        if specifications is not None:
            divs = specifications.find_all('div',class_='')
            for t in divs:
                try:
                    if t.find('div',class_='specItemTitle').text in ['Szerokość','Waga','Wysokość','Głębokość']:
                        features[t.find('div',class_='specItemTitle').text] = t.find('div',class_='specItemValue').text
                except:
                    pass
            for key, value in features.items():
                if isinstance(value,str):
                    try:
                        quantity, unit = value.split()
                        new_value = self.convertMetrics(quantity, unit)
                        features[key] = new_value
                    except:
                        features[key] = 0.0
        
        self.width = features['Szerokość']
        self.height = features['Wysokość']
        self.depth = features['Głębokość']
        self.weight = features['Waga']
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
            'Available for order': self.availableForOrder,
            'Width': self.width,
            'Height': self.weight,
            'Depth': self.depth,
            'Weight': self.weight
        }
    
    def convertMetrics(self, value, unit):
        units = {
            'mm': 0.01,
            'cm': 1.,
            'm': 100.0,
            'km': 1000.0,
            'g': 0.001,
            'kg': 1.0
        }
        if unit in units:
            return round(float(value) * units[unit],3)
        else:
            return 0.0
    
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
            for subCat in subCategories[:40]:
                nazwa = subCat.find('a').text
                if nazwa not in ['Akcesoria do czyszczenia','Grill i akcesoria grillowe', 'Mycie okien - akcesoria']:
                    self.subCategories.append(category(subCat,cat.categoryName, self.numberOfCategories))
                    self.numberOfCategories += 1

    def exportCategoriesToCsv(self):
        categories = []
        for cat in self.mainCategories:
            categories.append(cat.toDict())
        for cat in self.subCategories:
            #Deletion of empty categories
            if cat.numberOfProducts > 0:
                categories .append(cat.toDict())
        dataFrame = pd.DataFrame(categories)
        dataFrame.to_csv('../results/categories.csv', sep='>', encoding='utf-8')

    def searchPages(self, cat:category, numOfPages):
        for i in range(numOfPages):
            r = requests.get(f"{cat.link}?pre=0&pn={i}", headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')
            productLinks = soup.find_all('a', class_='site-product-link')
            for prod in productLinks:
                r = requests.get(f"{baseurl}{prod['href']}", headers=headers)
                soup = BeautifulSoup(r.content, 'lxml')
                p = product(soup, cat.categoryName, f"{cat.numberOfCategory}_{cat.numberOfProducts + 1}")
                if p.valid:
                    self.products.append(p.toDict())
                    cat.numberOfProducts += 1
                

    def scrapeProducts(self):
        for cat in self.subCategories:
            r = requests.get(f"{cat.link}?pre=0", headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')
            size = int(soup.find('div', class_='site-active-results-container').text.replace('Produkty w Twoim wyszukiwaniu: ',''))
            numOfPages = ceil(size/25)%2
            self.searchPages(cat, numOfPages)
        dataFrame = pd.DataFrame(self.products)
        dataFrame.to_csv('../results/products.csv', sep='>', encoding='utf-8')
    
    def scrape(self):
        self.scrapeMainCategories()
        self.scrapeSubCategories()
        self.scrapeProducts()
        self.exportCategoriesToCsv()

s = scraper()
s.scrape()
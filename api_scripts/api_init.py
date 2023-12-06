import re
import io
from copy import copy
from xml.etree import ElementTree
import prestapyt
import pandas as pd

URL = "http://localhost:8080/api"
KEY = "K2FBLL9JG9895G8HNG9A6CFTRMJP4Y2J"
headers = {
    'Content-Type': 'text/xml'
}
catids = {'Strona główna': 2}
prestashop = prestapyt.PrestaShopWebService(URL,KEY)
def addProductImages(prestashop, id, path):
    paths = path.split(';')
    for p in paths:
        index = p.rfind('/')
        filename = p[index + 1:]
        fd = io.open(f"../results/images/{filename}",'rb')
        content = fd.read()
        fd.close
        prestashop.add(f'/images/products/{id}', files=[("image",filename,content)])

def setQuantity(prestashop, id, quantity):
    stock = prestashop.get(f'stock_availables/{id}')
    stock.find('stock_available').find('quantity').text = str(quantity)
    prestashop.edit(f'stock_availables/{id}',ElementTree.tostring(stock))

def setCategories(prestashop, id, category):
    tree = prestashop.get(f'products/{id}')
    product = tree.find('product')
    product.remove(product.find('position_in_category'))
    product.remove(product.find('manufacturer_name'))
    product.remove(product.find('quantity'))
    try:
        product.find('associations').remove(product.find('associations').find('combinations'))
    except:
        pass
    associations = product.find('associations')
    associations.remove(associations.find('categories'))
    categories = ElementTree.SubElement(associations,'categories')
    cat = ElementTree.SubElement(categories,'category')
    id = ElementTree.SubElement(cat,'id')
    id.text = '2'
    cat = ElementTree.SubElement(categories,'category')
    id = ElementTree.SubElement(cat,'id')
    id.text = str(catids[category])
    prestashop.edit(f'products/{id}',ElementTree.tostring(tree))

def addCategories(prestashop):
    categories = pd.read_csv('../results/categories.csv', sep='>', encoding='utf-8')
    tree = prestashop.get('categories', options={'schema': 'blank'})
    for _, cat in categories.iterrows():
        ctree = copy(tree)
        category:ElementTree.Element = ctree.find('category')
        category.find('active').text=str(1)
        category.find('name').find('language').text=cat['Name']
        category.find('link_rewrite').find('language').text=cat['Name'].lower().replace(' ','-').replace(',','')
        category.find('id_parent').text=str(catids[cat['Parent category']])
        category.find('description').find('language').text=cat['Description']
        currentcat = prestashop.add('categories',ElementTree.tostring(ctree))
        catids[cat['Name']] = int(currentcat.find('category').find('id').text)

def addProducts(prestashop):
    products = pd.read_csv('../results/products.csv', sep='>', encoding='utf-8')
    tree = prestashop.get('products', options={'schema': 'blank'})
    for _, prod in products.iterrows():
        ptree = copy(tree)
        product:ElementTree.Element = ptree.find('product')
        try:
            product.remove(product.find('position_in_category'))
        except:
            pass
        try:
            product.find('associations').remove(product.find('associations').find('combinations'))
        except:
            pass
        product.find('name').find('language').text = prod['Name']
        product.find('id_category_default').text = str(catids[prod['Categories']])
        product.find('price').text = str(prod['Price tax excluded'])
        if prod['Description'] is str:
            product.find('description').find('language').text = prod['Description']
        product.find('available_for_order').text = str(prod['Available for order'])
        product.find('id_shop_default').text = '1'
        product.find('id_tax_rules_group').text = '1'
        product.find('active').text = '1'
        product.find('state').text = '1'
        product.find('minimal_quantity').text = '1'
        product.find('show_price').text = '1'
        product.find('link_rewrite').find('language').text = re.sub(r"[^a-zA-Z0-9]+", "-",prod['Name']).lower()
        product.find('meta_title').find('language').text = prod['Name']
        product.find('width').text = str(prod['Width'])
        product.find('height').text = str(prod['Height'])
        product.find('depth').text = str(prod['Depth'])
        product.find('weight').text = str(prod['Weight'])
        id = prestashop.add('products', ElementTree.tostring(ptree)).find('product').find('id').text
        setCategories(prestashop, id, prod['Categories'])
        setQuantity(prestashop, id, prod['Quantity'])
        addProductImages(prestashop,id,prod['Image URLs'])

def deleteAllProducts(prestashop):
    products = prestashop.get('products').find('products').findall('product')
    for p in products:
        prestashop.delete('products',resource_ids=p.attrib['id'])

def deleteAllCategories(prestashop):
    categories = prestashop.get('categories').find('categories').findall('category')
    cids = []
    for c in categories:
        if int(c.attrib['id'])>2:
            cids.append(c.attrib['id'])
    try:
        prestashop.delete('categories',cids)
    except Exception as e:
        print(f"Błąd usuwania: {e}")

deleteAllCategories(prestashop)
deleteAllProducts(prestashop)
addCategories(prestashop)
addProducts(prestashop)
from bs4 import BeautifulSoup
import csv
import requests
import time


url = requests.get('http://books.toscrape.com').text
soup = BeautifulSoup(url, 'lxml')

def scour_category(url_category):
    url = requests.get(url_category).text
    soup = BeautifulSoup(url, 'lxml')
    book_list = soup.find_all('div', class_ = 'image_container')
    for book in book_list:
        info = book.find('a')
        link = 'http://books.toscrape.com/catalogue/' + info['href'].replace('../../../', '')
        print(link)
        

#scour_category('http://books.toscrape.com/catalogue/category/books/travel_2/index.html')

def listing_categories():
    url = requests.get('http://books.toscrape.com').text
    soup = BeautifulSoup(url, 'lxml')
    categ_list = soup.find('ul', class_ = 'nav nav-list').find('ul').find_all('li')
    i = 0
    for category in categ_list:
        name = categ_list[i].text.strip()
        rough_link = categ_list[i].find('a')
        link = rough_link['href']
        print('http://books.toscrape.com/' + link)
        with open(f'{name}.csv', 'w', newline = '', encoding = 'utf-8') as csvfile:
            fieldname = ['product_page_url', 'universal_ product_code (upc)', 'title',
                         'price_including_tax', 'price_excluding_tax', 'number_available',
                         'product_description', 'category', 'review_rating', 'image_url']
            writer = csv.writer(csvfile)
            writer.writerow(fieldname)
        i = i +1
#We sleep for 3 seconds, so we don't get flagged as a bot
        time.sleep(3)

listing_categories()

def extract_book(url_book):
    url = 'http://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html'
#Ne pas oublier le .text
    response = requests.get('http://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html').text
    soup = BeautifulSoup(response, 'lxml')

#Prépare l'exploitation de plusieurs des données nécessaires
    info_table = soup.find('table', class_ = 'table table-striped')
    info_list = info_table.find_all('td')

#product_page_url


#universal_product_code(upc)
    upc = info_list[0].text

#title
    title = soup.find('li', class_ = 'active').text

#price_including_tax
    price_wtax = info_list[3].text.replace('Â', '')

#price_excluding_tax
    price_wotax = info_list[2].text.replace('Â', '')

#number_available
# If the book is in stock, we first strip irrelevant information to find the number.
    if 'In stock' in info_list[5].text:
        availability = info_list[5].text.replace('(', '').split()
        amount = availability[2]
    else:
        amount = '0'

#product_description
    desc = soup.find('p', {'class': ''}).text

#category
    categ_strip = soup.find('ul', class_ = 'breadcrumb').text.split()
    category = categ_strip[2]

#review_rating
    rating = soup.find('p', class_ = 'star-rating')
    review_rating = rating['class'][1]

#image_url
    img_tag = soup.find('img')
    img_url = img_tag['src'].replace('../..', '')
    cover = 'http://books.toscrape.com' + img_url

    with open('scrape.csv', 'w', newline = '', encoding = 'utf-8') as csvfile:
        fields = [url, upc, title, price_wtax, price_wotax, amount, desc, category, review_rating, cover]
        fieldname = ['product_page_url', 'universal_ product_code (upc)', 'title',
                     'price_including_tax', 'price_excluding_tax', 'number_available',
                     'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.writer(csvfile)
        writer.writerow(fieldname)
        writer.writerow(fields)

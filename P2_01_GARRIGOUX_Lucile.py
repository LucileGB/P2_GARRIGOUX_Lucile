from bs4 import BeautifulSoup
import csv
import os
import requests
#import time

#### Global variables
url = requests.get('http://books.toscrape.com').text
soup = BeautifulSoup(url, 'lxml')
cat_name = 'To be filled'


###### EXTRACTING DATA FROM A BOOK PAGE
def extract_book(url_book):
    url = url_book
    response = requests.get(url_book).text
    soup = BeautifulSoup(response, 'lxml')

    info_table = soup.find('table', class_ = 'table table-striped')
    info_list = info_table.find_all('td')

    upc = info_list[0].text
    title = soup.find('li', class_ = 'active').text
    price_wtax = info_list[3].text.replace('Â£', '')
    price_wotax = info_list[2].text.replace('Â£', '')

    if 'In stock' in info_list[5].text:
        availability = info_list[5].text.replace('(', '').split()
        amount = availability[2]
    else:
        amount = '0'

    if soup.find('p', {'class': ''}):
        desc = soup.find('p', {'class': ''}).text
    else:
        desc = "No description."

    categ_strip = soup.find('ul', class_ = 'breadcrumb').text.split()
    category = categ_strip[2]
    ratings = soup.find('p', class_ = 'star-rating')
    review_rating = ratings['class'][1]

#Isolating the cover URL and downloading the cover
    img_tag = soup.find('img')
    img_url = img_tag['src'].replace('../..', '')
    cover = 'http://books.toscrape.com' + img_url
    
    download_cover = requests.get(cover)
    with open(f'covers\{upc}.jpg', 'wb') as picture:
        picture.write(download_cover.content)

# Finally, we input our results in the relevant csv file.
    with open(f'{cat_name}.csv', 'a+', newline = '', encoding = 'utf-8') as csvfile:
        fields = [url, upc, title, price_wtax, price_wotax, amount, desc, category, review_rating, cover]
        writer = csv.writer(csvfile)
        writer.writerow(fields)


#### SCOURING A CATEGORY'S PAGE AND GOING TO NEXT       
#Scouring a page is separate from scouring a category
#so we can reuse url_category to go to the next page.
def scour_page(url_page, url_category):
    url = requests.get(url_page).text
    soup = BeautifulSoup(url, 'lxml')
    book_list = soup.find_all('div', class_ = 'image_container')
    
    for book in book_list:
        info = book.find('a')
        link = 'http://books.toscrape.com/catalogue/' + info['href'].replace('../../../', '')
        print(link)
        extract_book(link)
#        time.sleep(3)

# Go to the next page if there is one.
    has_next = soup.find('li', class_ = 'next')
    if has_next:
        next_page = has_next.find('a')
        np_link = url_category + next_page['href']
        scour_page(np_link, url_category)


####SCOURING A CATEGORY
# Mostly calls scour_page.
def scour_category(url_category):
    url = requests.get(url_category).text
    soup = BeautifulSoup(url, 'lxml')
    scour_page(url_category, url_category)

#### MAIN
def main():
    os.mkdir('covers')
    url = requests.get('http://books.toscrape.com').text
    soup = BeautifulSoup(url, 'lxml')
    categ_list = soup.find('ul', class_ = 'nav nav-list').find('ul').find_all('li')
    i = 0

# Create a CSV for each new category
    for category in categ_list:
        global cat_name
        cat_name = categ_list[i].text.strip()
        with open(f'{cat_name}.csv', 'w', newline = '', encoding = 'utf-8') as csvfile:
            fieldname = ['product_page_url', 'universal_ product_code (upc)', 'title',
                         'price_including_tax', 'price_excluding_tax', 'number_available',
                         'product_description', 'category', 'review_rating', 'image_url']
            writer = csv.writer(csvfile)
            writer.writerow(fieldname)

# Calls to scour_category
        raw_link = categ_list[i].find('a')
        link = raw_link['href'].replace('index.html', '')
        scour_category('http://books.toscrape.com/' + link)
        print('http://books.toscrape.com/' + link)
        i = i +1
#        time.sleep(3)

main()

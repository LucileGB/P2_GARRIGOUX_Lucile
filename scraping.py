from bs4 import BeautifulSoup
import argparse
import csv
import os
from pathlib import Path
import requests
import time

#url = requests.get("http://books.toscrape.com").text

class Scraper:
    def __init__(self, delay):
        self.delay = delay
        self.root_url = "http://books.toscrape.com"
        self.root_response = requests.get(self.root_url).text
        self.categ_folder = Path("categories/")


    def init_scraping(self):
        soup = BeautifulSoup(self.root_response, "lxml")
        categ_list = soup.find("ul", class_="nav nav-list").find("ul").find_all("li")

        try:
            os.mkdir("covers")
            os.mkdir("categories")
        except FileExistsError:
            pass

        for category in categ_list:
            self.category_set_up(category)


    def category_set_up(self, category):
        """
        Initializes a CSV file for the chosen category, then calls
        scrape_category.
        """
        category_name = category.text.strip()
        raw_link = category.find("a")
        link = raw_link["href"].replace("index.html", "")
        csv_path = self.categ_folder / f"{category_name}.csv"

        with open(csv_path, "w", newline="") as csvfile:
            fieldnames = [
                "product_page_url",
                "universal_ product_code (upc)",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url",
            ]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

        self.scrape_category(f"{self.root_url}/{link}", csv_path)


    def scrape_category(self, url, category_csv):
        """
        Calls scrape_page and stores url_category.
        """
        response = requests.get(url).text
        soup = BeautifulSoup(response, "lxml")
        self.scrape_page(1, url, category_csv)


    def scrape_page(self, i, category_url, category_csv):
        """
        Calls scrape_book for each book link. Calls itself for the next page,
        as long as there is one.
        """
        page_url = f"{category_url}page-{i}.html"
        response = requests.get(page_url).text
        soup = BeautifulSoup(response, "lxml")
        book_list = soup.find_all("div", class_="image_container")
        has_next = soup.find("li", class_="next")

        for book in book_list:
            info = book.find("a")
            url = "http://books.toscrape.com/catalogue/" + info["href"].replace(
                "../../../", ""
            )
            self.scrape_book(url)

            if delay > 0:
                time.sleep(delay)

        if has_next:
            i += 1
            self.scrape_page(i, category_url, category_csv)


    def scrape_book(self, url):
        """
        Scrapes the content of an individual book page.
        """
        response = requests.get(url)
        response.encoding = "UTF-8"
        soup = BeautifulSoup(response.text, "lxml")

        info_table = soup.find("table", class_="table table-striped")
        info_list = info_table.find_all("td")

        amount = 0
        category = soup.find("ul", class_="breadcrumb").find_all("li")[2]
        category = category.text.strip()
        desc = "No description."
        img_url = soup.find("img")["src"].replace("../..", "")

        if "In stock" in info_list[5].text:
            amount = info_list[5].text.replace("(", "").split()[2]

        if soup.find("p", {"class": ""}):
            desc = soup.find("p", {"class": ""}).text

        book = {
            'url': url,
            'upc': info_list[0].text,
            'title': soup.find("li", class_="active").text,
            'price_wtax': info_list[3].text,
            'price_wotax': info_list[2].text,
            'amount': amount,
            'desc': desc,
            'category': category,
            'review_rating': soup.find("p", class_="star-rating")["class"][1],
            'cover': f"{self.root_url}{img_url}"
        }

        self.save_cover(book)

        return book


    def save_cover(self, book):
        cover_path = Path("covers/") / f"{book['upc']}.jpg"
        cover_file = requests.get(book['cover']).content

        with open(cover_path, "wb") as picture:
            picture.write(cover_file)


    def save_book(self, book):
        with open(saved_cover, "a+", newline="", errors="ignore") as csvfile:
            values = list(book.values())
            writer = csv.writer(csvfile)
            writer.writerow(values)

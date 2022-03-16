from bs4 import BeautifulSoup
import csv
import os
from pathlib import Path
import requests

from time import sleep

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
        Initializes a CSV file for the category, then calls scrape_category.
        """
        category_name = category.text.strip()
        raw_url = category.find("a")
        url = raw_url["href"].replace("index.html", "")
        csv_path = self.categ_folder / f"{category_name}.csv"

        with open(csv_path, "w", newline="") as csv_file:
            field_names = [
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
            writer = csv.writer(csv_file)
            writer.writerow(field_names)

        self.scrape_category(1, f"{self.root_url}/{url}", csv_path)
        print(f"La catégorie \"{category_name}\" est terminée.")


    def scrape_category(self, i, category_url, category_csv):
        """
        A recursive function which will call itself for each next page to
        scrape, as long as there is one. For each page, creates a list of
        scraped books and then writes it into the category CSV.
        """
        if i == 1:
            page_url = category_url
        else:
            page_url = f"{category_url}page-{i}.html"

        response = requests.get(page_url).text
        soup = BeautifulSoup(response, "lxml")
        book_list = soup.find_all("div", class_="image_container")
        has_next = soup.find("li", class_="next")
        scraped_books = []

        for book in book_list:
            details = book.find("a")["href"].replace("../../../", "")
            url = f"{self.root_url}/catalogue/{details}"
            scraped = self.scrape_book(url)
            scraped_books.append(scraped)

            if self.delay > 0:
                sleep(self.delay)

        self.save_books(category_csv, scraped_books)

        if has_next:
            i += 1
            self.scrape_category(i, category_url, category_csv)


    def scrape_book(self, url):
        """
        Scrapes the content of an individual book page, returning it as a
        dictionary.
        Also saves the cover in the 'covers' folder.
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
            "url": url,
            "upc": info_list[0].text,
            "title": soup.find("li", class_="active").text,
            "price_wtax": info_list[3].text,
            "price_wotax": info_list[2].text,
            "amount": amount,
            "desc": desc,
            "category": category,
            "review_rating": soup.find("p", class_="star-rating")["class"][1],
            "cover": f"{self.root_url}{img_url}"
        }

        self.save_cover(book)

        return book


    def save_cover(self, book):
        cover_path = Path("covers/") / f"{book['upc']}.jpg"
        cover_file = requests.get(book['cover']).content

        with open(cover_path, "wb") as picture:
            picture.write(cover_file)


    def save_books(self, categ_csv, book_list):
        with open(categ_csv, "a+", newline="", errors="ignore", encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)

            for book in book_list:
                values = list(book.values())
                writer.writerow(values)

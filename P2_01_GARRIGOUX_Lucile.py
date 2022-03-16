from bs4 import BeautifulSoup
import argparse
import csv
import os
from pathlib import Path
import requests
import time

#url = requests.get("http://books.toscrape.com").text
delay = 0

class Scraper:
    def __init__(self):
        self.root_url = "http://books.toscrape.com"
        self.root_response = requests.get(root_url).text
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
        Initialize a CSV file for the chosen category, then calls
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

        scrape_category(f"http://books.toscrape.com/{link}")


    def scrape_category(self, url):
        """Calls scour_page and stores url_category."""
        response = requests.get(url_category).text
        soup = BeautifulSoup(response, "lxml")
        scour_page(url, url)


    def scour_page(url_page, url_category):
        """Calls extract_book for each book link. Calls itself for the next page."""
        url = requests.get(url_page).text
        soup = BeautifulSoup(url, "lxml")
        book_list = soup.find_all("div", class_="image_container")
        has_next = soup.find("li", class_="next")

        for book in book_list:
            info = book.find("a")
            link = "http://books.toscrape.com/catalogue/" + info["href"].replace(
                "../../../", ""
            )
            extract_book(link)

            if delay > 0:
                time.sleep(delay)

        if has_next:
            next_page = has_next.find("a")
            np_link = url_category + next_page["href"]
            scour_page(np_link, url_category)


def extract_book(url_book):
    """scrape the content of an individual book page"""
    url = url_book
    response = requests.get(url_book)
    response.encoding = "UTF-8"
    soup = BeautifulSoup(response.text, "lxml")

    info_table = soup.find("table", class_="table table-striped")
    info_list = info_table.find_all("td")

    upc = info_list[0].text
    title = soup.find("li", class_="active").text
    price_wtax = info_list[3].text
    price_wotax = info_list[2].text

    if "In stock" in info_list[5].text:
        availability = info_list[5].text.replace("(", "").split()
        amount = availability[2]
    else:
        amount = "0"

    if soup.find("p", {"class": ""}):
        desc = soup.find("p", {"class": ""}).text
    else:
        desc = "No description."

    categ_strip = soup.find("ul", class_="breadcrumb").text.split()
    category = categ_strip[2]
    ratings = soup.find("p", class_="star-rating")
    review_rating = ratings["class"][1]
    img_tag = soup.find("img")
    img_url = img_tag["src"].replace("../..", "")
    cover = self.root_url + img_url

    download_cover = requests.get(cover)
    cover_folder = Path("covers/")
    saved_cover = cover_folder / f"{upc}.jpg"
    with open(saved_cover, "wb") as picture:
        picture.write(download_cover.content)

    with open(saved_cover, "a+", newline="", errors="ignore") as csvfile:
        fields = [
            url,
            upc,
            title,
            price_wtax,
            price_wotax,
            amount,
            desc,
            category,
            review_rating,
            cover,
        ]
        writer = csv.writer(csvfile)
        writer.writerow(fields)



def main():
    """Main function. Creates cover directory/csv files and calls scour_category."""
    start = int(time.time())
    print(f"Scraping commencé à {time.strftime('%T')}...")


    if delay > 0:
        time.sleep(delay)

    end = time.time()
    duration = int(end - start)

    print(f"Scraping terminé à {time.strftime('%T')}.")
    print(f"Durée : {duration} secondes, soit {round(duration/60)} minutes.")


"""Allow the user to set the delay between two book scrapes if wished."""
parser = argparse.ArgumentParser()
parser.add_argument(
    "--delay",
    help="Intervalle entre chaque scrape de livre (unité de base en seconde).",
    type=float,
)
args = parser.parse_args()
if args.delay:
    if args.delay > 0:
        delay = float(args.delay)
        main()
    else:
        main()
else:
    main()

truc = Scraper()
truc.init_scraping()

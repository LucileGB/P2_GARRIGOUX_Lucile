from bs4 import BeautifulSoup
import argparse
import csv
import os
import requests
import time

url = requests.get("http://books.toscrape.com").text
soup = BeautifulSoup(url, "lxml")
cat_name = "To be filled"
secs = 0


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
    cover = "http://books.toscrape.com" + img_url

    download_cover = requests.get(cover)
    with open(f"covers\{upc}.jpg", "wb") as picture:
        picture.write(download_cover.content)

    with open(f"{cat_name}.csv", "a+", newline="", errors="ignore") as csvfile:
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

        if secs > 0:
            time.sleep(secs)

    if has_next:
        next_page = has_next.find("a")
        np_link = url_category + next_page["href"]
        scour_page(np_link, url_category)


def scour_category(url_category):
    """Calls scour_page and stores url_category."""
    url = requests.get(url_category).text
    soup = BeautifulSoup(url, "lxml")
    scour_page(url_category, url_category)


def main():
    """Main function. Creates cover directory/csv files and calls scour_category."""
    start = int(time.time())
    print(f"Scraping commencé à {time.strftime('%T')}...")
    os.mkdir("covers")
    url = requests.get("http://books.toscrape.com").text
    soup = BeautifulSoup(url, "lxml")
    categ_list = soup.find("ul", class_="nav nav-list").find("ul").find_all("li")
    i = 0

    for category in categ_list:
        global cat_name
        cat_name = categ_list[i].text.strip()
        with open(f"{cat_name}.csv", "w", newline="") as csvfile:
            fieldname = [
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
            writer.writerow(fieldname)

        raw_link = categ_list[i].find("a")
        link = raw_link["href"].replace("index.html", "")
        scour_category("http://books.toscrape.com/" + link)
        i = i + 1

    end = time.time()
    duration = int(end - start)

    print(f"Scraping terminé à {time.strftime('%T')}.")
    print(f"Durée : {duration} secondes, soit {round(duration/60)} minutes.")


"""Calls main() only if the delay between two book scrapes has been set to 0 or
to a valid integer."""
parser = argparse.ArgumentParser()
parser.add_argument(
    "--secs",
    help="Delay between two books scrapes (in seconds, from 1 onward.)",
    type=int,
)
args = parser.parse_args()
if args.secs:
    if args.secs >= 0:
        secs = args.secs
        main()
    else:
        print("Please input a number superior to 0.")

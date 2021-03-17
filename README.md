_**Note:** this scraper is actually a school exercise. This code is not the best you can find for an efficient scraper._

<h1>Webscraper for the "Book for Scrape" website</h1>
<h2>Features</h2>
This tool scrapes the online bookseller _Book to Scrape_  and retrieves the following informations from every book:

    product_page_url
    universal_ product_code (upc)
    title
    price_including_tax
    price_excluding_tax
    number_available
    product_description
    category
    review_rating
    image_url

It also downloads every cover in a separate "cover" folder. Cover are named after the upc of each book, so each file name is truly unique.

The data is sorted in one csv file per category. Please note that prices are in pound.

<h2>Installation and usage</h2>
Relevant library versions can be installed from requirement.txt.

The program starts as soon as launched.

If wished or needed, you can remove the # from before _import time_ and from before the two _time.sleep(3)_ lines in the code so as to slow the scraper down, emulating a more "natural" user's behavior. The _3_ signifies a wait of 3 seconds, but you can freely modify this value.

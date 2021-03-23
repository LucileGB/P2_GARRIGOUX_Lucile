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

The data is sorted in one csv file per category.

You can set a delay between two book scrapes.

<h2>Installation</h2>
<h3>(Optional) Installing a virtual environment</3>
If wished, you can install a virtual environment to run the app. First, use the console to install virtualenv:

    pip install virtualenv

Then, use the console to navigate to the folder where you want to run your virtual environment (and the app) and type the following command:

    virtualenv DIRECTORYNAME
    
The directory's name can be anything you wish. Then, activate your virtual environment by typing the following:

    DIRECTORYNAME\Scripts\activate
    
You'll see that the prompt prefixing your console location will change, for instance like so:

_C:\Users\LG\Documents\Projet 2>_ scraper\Scripts\activate

_**(scraper)** C:\Users\LG\Projet 2>_

You are now inside of your virtual environment. Any library installation will take place inside this library

<h3>Installing libraries</3>
To install the necessary libraries, use the console to navigate to the directory where you downloaded the app and its requirement.txt files. Then, type the following into the console:

    pip install -r requirements.txt

Pip will then install them.

<h2>Usage</h2>
Once the installation is complete, you can launch the app "as is". While in the console, navigate to the app's directory then type the following:

    P2_01_GARRIGOUX_Lucile.py

You can also set a delay between two book scrapes. To do so, input the following, where NUMBER is a positive integer:

    P2_01_GARRIGOUX_Lucile.py --secs NUMBER

For exemple:
![image](https://user-images.githubusercontent.com/72474020/112191219-17af7800-8c06-11eb-9bc9-30e123acd633.png)

This will start the program. A "Cover" directory and the category's CSV files will be created in the app's directory.

The program will print a message upon completion.

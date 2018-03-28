"""
A simple image downloader for poorlydrawnlines.com/archive
"""
import time
import os
import sys
import re
import concurrent.futures


import requests
from bs4 import BeautifulSoup as bs


DEFAULT_DIR_NAME = "poorly_created_folder"
COMICS_DIRECTORY = os.path.join(os.getcwd(), DEFAULT_DIR_NAME)


LOGO = """
a Python comic(al) scraper for poorlydwarnlines.com
                         __
.-----.-----.-----.----.|  |.--.--.
|  _  |  _  |  _  |   _||  ||  |  |
|   __|_____|_____|__|  |__||___  |
|__|                        |_____|
                __ __   __
.--.--.--.----.|__|  |_|  |_.-----.-----.
|  |  |  |   _||  |   _|   _|  -__|     |
|________|__|  |__|____|____|_____|__|__|

.-----.----.----.---.-.-----.-----.----.
|__ --|  __|   _|  _  |  _  |  -__|   _|
|_____|____|__| |___._|   __|_____|__|
                      |__|
version: 0.4 | author: baduker | https://github.com/baduker
"""


ARCHIVE_URL = "http://www.poorlydrawnlines.com/archive/"
COMIC_PATTERN = re.compile(r'http://www.poorlydrawnlines.com/comic/.+')

def download_comics_menu(comics_found):
    """
    Main download menu, takes number of available comics for download
    """
    print("\nThe scraper has found {} comics.".format(len(comics_found)))
    print("How many comics do you want to download?")
    print("Type 0 to exit.")

    while True:
        try:
            comics_to_download = int(input(">> "))
        except ValueError:
            print("Error: expected a number. Try again.")
            continue
        if comics_to_download > len(comics_found) or comics_to_download < 0:
            print("Error: incorrect number of comics to download. Try again.")
            continue
        elif comics_to_download == 0:
            sys.exit()
        return comics_to_download


def grab_image_src_url(session, url):
    """
    Fetches urls with the comic image source
    """
    response = session.get(url)
    soup = bs(response.text, 'html.parser')
    for i in soup.find_all('p'):
        for img in i.find_all('img', src=True):
            return img['src']


def download_and_save_comic(session, url):
    """
    Downloads and saves the comic image
    """
    file_name = url.split('/')[-1]
    with open(os.path.join(COMICS_DIRECTORY, file_name), "wb") as file:
        response = session.get(url)
        file.write(response.content)


def fetch_comics_from_archive(session):
    """
    Grabs all urls from the poorlydrawnlines.com/archive and parses for only those that link to published comics
    """
    response = session.get(ARCHIVE_URL)
    soup = bs(response.text, 'html.parser')
    comics = [url.get("href") for url in soup.find_all("a")]
    return [url for url in comics if COMIC_PATTERN.match(url)]


def download_comic(session, url):
    """
    Download progress information
    """
    print("Downloading: {}".format(url))
    url = grab_image_src_url(session, url)
    download_and_save_comic(session, url)


def main():
    """
    Encapsulates and executes all methods in the main function
    """
    print(LOGO)

    session = requests.Session()

    comics = fetch_comics_from_archive(session)
    comics_to_download = download_comics_menu(comics)

    try:
        os.mkdir(DEFAULT_DIR_NAME)
    except OSError as exc:
        sys.exit("Failed to create directory (error_no {})".format(exc.error_no))

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda url: download_comic(session, url), comics[:comics_to_download])
    executor.shutdown()
    end = time.time()
    print("Finished downloading {} comics in {:.2f} sec.".format(comics_to_download, end - start))

if __name__ in "__main__":
    main()

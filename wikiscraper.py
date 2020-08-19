import requests
from bs4 import BeautifulSoup
import os

wikiurl = 'https://en.wikipedia.org/'

# given a Wikipedia category URL, this returns a potential next page url if one exists
# otherwise, it returns None
# also writes all titles of pages in current open file
def get_titles(url, file):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    #check if it fails
    pages = soup.find("div", {'id': "mw-pages"})

    titles = pages.find_all('li')
    for title in titles:
        file.write(title.text.strip())
        file.write('\n')

    nexturl = None
    links = soup.find_all('a')
    for link in links:
        if link.text == 'next page':
            nexturl = wikiurl + link.get('href')

    return nexturl

# given the first link (the seedurl), this function will get all the titles starting with
# this page and create a file with all the titles in it
def write_title_file(seedurl, path):
    page = requests.get(seedurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    filename = soup.find(id="firstHeading").text.replace('Category:', '')
    print(filename)
    file = open(path + "/" + filename + ".txt", 'w')
    nexturl = get_titles(seedurl, file)
    while nexturl is not None:
        nexturl = get_titles(nexturl, file)

def decade_iterator(parent_dir, country, url1, url2):
    # go through every decade
    year = 1990
    while year <= 2010:
        path = os.path.join(parent_dir, str(year))
        path = os.path.join(path, country)
        url = url1 + str(year) + url2
        write_title_file(url, path)
        year += 10

decade_iterator("/Users/dorothyqu/PycharmProjects/thesis/decades", "Australia", "https://en.wikipedia.org/wiki/Category:", "s_Australian_animated_television_series")
import os

# build a directory made like:
# decades
# countries
# categories/topics as files? or maybe folders

parent_dir = "/Users/dorothyqu/PycharmProjects/thesis/decades"

def make_decades(parent_dir):
    os.mkdir(parent_dir)
    # make the decades
    year = 1950
    while year <= 2020:
        path = os.path.join(parent_dir, str(year))
        os.mkdir(path)
        make_countries(path)
        year += 10

def make_countries(parent_dir):
    with open('countries.txt') as file:
        countries = file.readlines()

    for country in countries:
        country = country.strip()
        path = os.path.join(parent_dir, country)
        os.mkdir(path)

def add_countries(parent_dir, country):
    year = 1950
    while year <= 2020:
        path = os.path.join(parent_dir, str(year))
        path = os.path.join(path, country)
        os.mkdir(path)
        year += 10

#make_decades(parent_dir)

add_countries(parent_dir, "Australia")
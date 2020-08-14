from bs4 import BeautifulSoup
import lxml
import requests

def scrape_game_details(name, platform):
    details = {"name":"", "platform":"", "release_data":"","vote":{"critic":"", "user":""}, "product_details":{"rating":"", "developer":"", "genres":[], "number_of_online_players":"No Online Multiplayer"}}
    url = "https://www.metacritic.com/game"
    url += "/" + platform
    url += "/" + parse_name(name)
    url += "/details"
    try:
        req = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(req.text, 'lxml')
        details['name'] = name
        details['platform'] = platform
        get_score(soup, details)
        get_details(soup, details)
        details['release_data'] = get_release_data(soup)
        print(details)
    except IndexError as err:
        print("ERROR " + str(err))
    
def parse_name(name):
    name = name.strip()
    name = name.lower()
    name = name.replace(" ","-")
    return name

def get_score(page, details):
    alinks = page.find_all("a","metascore_anchor")
    #print(alinks)
    for a in alinks:
        if details['vote']['user'] == "" and "user" in a.div['class']:
            details['vote']['user'] = get_user_score(a)
        elif details['vote']['critic'] == "" and "large" in a.div['class']:
            details['vote']['critic'] = get_critic_score(a)
        elif details['vote']['user'] != "" and details['vote']['critic'] != "":
            return

    if details['vote']['critic'] == "":
        details['vote']['critic'] = "no score yet"
    if details['vote']['user'] == "":
        details['vote']['user'] = "no score yet"
    
def get_critic_score(tag):
    try:
        critic_score = int(tag.div.span.string)
    except ValueError as err:
        critic_score = "no score yet"
    return critic_score

def get_user_score(tag):
    try:
        user_score = float(tag.div.string)
    except ValueError as err:
        user_score = "no score yet"
    return user_score

def get_release_data(page):
    return page.find("li", "release_data").contents[3].string

def get_details(page, details):
    #print(get_description(page))
    get_product_details(page, details)

def get_description(page):
    print("\n\nsummary detail")
    desc = page.find("span","data")
    return desc

def get_product_details(page, details):
    table_headers = page.find_all("th")
    for th in table_headers:
        find_details(th, details)

def find_details(th, details):
    if(th.string == "Rating:"):
        details['product_details']['rating'] = th.find_next_sibling("td").string
    elif(th.string == "Developer:"):
        details['product_details']['developer'] = th.find_next_sibling("td").string
    elif(th.string == "Genre(s):"):
        parse_genres(str(th.find_next_sibling("td").string), details)
    elif(th.string == "Number of Online Players:"):
        details['product_details']['number_of_online_players'] = th.find_next_sibling("td").string

def parse_genres(td, details):
    genres = td.split(',')
    for genre in genres:
        details['product_details']['genres'].append(genre.strip())

scrape_game_details("Death Stranding", "pc")
scrape_game_details("Red Dead Redemption 2", "playstation-4")
scrape_game_details("just dance 2017", "wii-u")
scrape_game_details("halo 4", "xbox-360")
scrape_game_details("resistance 2", "playstation-3")
scrape_game_details("the last of us", "playstation-3")
scrape_game_details("skully", "playstation-4")
scrape_game_details("overwatch", "pc")

platforms = ["pc","playstation-4","xbox-one","playstation-3","xbox-360","playstation-2","xbox","playstation","psp","playstation-5","xbox-series-x","playstation-vita","switch","wii","wii-u","3ds","stadia","ios"]
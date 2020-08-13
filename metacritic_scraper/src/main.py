from bs4 import BeautifulSoup
import numpy as np
import lxml
import requests

details = {'name': str, 'platform':str, 'release_date':str, 'vote':{"critic": int, "user": float}, "product_details":{'rating' : str, 'developer' : str, 'genres' : [], "number_of_online_players":int}}

def scrape_details(url):
    url += "/details"
    try:
        req = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(req.text, 'lxml')
        get_score(soup)
        get_details(soup)
        #details['name'] = "death stranding"
        details['platform'] = "ps4"
        #print(soup.find("span","count").descendants)
        print(details)
    except IndexError as err:
        print("ERROR " + str(err))
    
def get_score(page):
    a = page.find_all("a","metascore_anchor")
    details['vote']['critic'] = get_critic_score(a[0])
    details['vote']['user'] = get_user_score(a[1])
    
def get_critic_score(tag):
    return int(tag.div.span.string)

def get_user_score(tag):
    return float(tag.div.string)

def get_details(page):
    #print(get_description(page))
    get_product_details(page)

def get_description(page):
    print("\n\nsummary detail")
    desc = page.find("span","data")
    return desc

def get_product_details(page):
    table_headers = page.find_all("th")
    for th in table_headers:
        find_details(th)

def find_details(th):
    if(th.string == "Rating:"):
        details['product_details']['rating'] = th.find_next_sibling("td").string
    elif(th.string == "Developer:"):
        details['product_details']['developer'] = th.find_next_sibling("td").string
    elif(th.string == "Genre(s):"):
        parse_genres(str(th.find_next_sibling("td").string))
    elif(th.string == "Number of Online Players:"):
        details['product_details']['number_of_online_players'] = th.find_next_sibling("td").string

def parse_genres(td):
    genres_parsed = np.core.defchararray.split(td.strip(), sep=",")
    genres = np.array(list(genres_parsed))
    for genre in genres:
        details['product_details']['genres'].append(genre.strip())

url = "https://www.metacritic.com/game/playstation-4/death-stranding"

scrape_details(url)

print("\n")

url = "https://www.metacritic.com/game/pc/death-stranding"

scrape_details(url)



platforms = ["pc","playstation-4","xbox-one","playstation-3","xbox-360","playstation-2","xbox","playstation","psp","","psp"]
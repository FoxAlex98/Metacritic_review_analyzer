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
    name = name.replace(": ","-")
    name = name.replace(" ","-")
    return name

def get_score(page, details):
    critic_score = page.select_one("div.metascore_wrap.feature_metascore")
    get_critic_score(critic_score,details)

    user_score = page.select_one("div.metascore_w.user.large.game")
    get_user_score(user_score,details)
    
def get_critic_score(critic_score,details):
    critic_score = critic_score.a.div
    if critic_score is not None:
        details['vote']['critic'] = critic_score.text
    else:
        details['vote']['critic'] = "To be determined"

def get_user_score(user_score,details):
    if user_score is not None:
        details['vote']['user'] = user_score.text
        if user_score.text != "tbd":
            return
    details['vote']['user'] = "To be determined"

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
from bs4 import BeautifulSoup
import lxml
import requests
import pandas as pd
import progressbar

def scrape_game_reviews(name, platform):
    reviews = {"critic", "user"}
    url = "https://www.metacritic.com/game"
    url += "/" + platform
    url += "/" + parse_name(name)
    url += "/user-reviews"
    try:
        req = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(req.text, 'lxml')
        try:
            pages = soup.find("li","last_page")
            if pages is None:
                last_page = 1
            else:
                last_page = int(pages.text)
        except ValueError as err:
            last_page = int((soup.find("li","last_page").text).replace("…",""))
        scrape(url, last_page)
    except IndexError as err:
        print("ERROR " + str(err))

def parse_name(name):
    name = name.strip()
    name = name.lower()
    name = name.replace(": ","-")
    name = name.replace(" ","-")
    return name

def scrape(url, last_page):
    review_dict = {'name':[], 'date':[], 'rating':[], 'review':[]}
    print(str(last_page) + " page to scan")
    bar = progressbar.ProgressBar(maxval=last_page, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for x in range(last_page):
        bar.update(x+1)
        #print("scanning page number " + str(x+1))
        req = requests.get(url + "?page=" + str(x), headers={'User-agent': 'Mozilla/5.0'})
        page = BeautifulSoup(req.text, 'lxml')
        for review in page.find_all('div', class_='review_content'):
            if review.find('div', class_='name') == None:
                break 
            review_dict['name'].append(review.find('div', class_='name').find('a').text)
            review_dict['date'].append(review.find('div', class_='date').text)
            review_dict['rating'].append(int(review.find('div', class_='review_grade').find_all('div')[0].text))
            try:
                if review.find('span', class_='blurb blurb_expanded'):
                    review_dict['review'].append(review.find('span', class_='blurb blurb_expanded').text)
                else:
                    review_dict['review'].append(review.find('div', class_='review_body').find('span').text)
            except AttributeError as err:
                review_dict['review'].append(" ")

    bar.finish()
    user_reviews = pd.DataFrame(review_dict)

    print(user_reviews[['name','date','rating']])

    avg = float(sum(user_reviews['rating'])/len(user_reviews['rating']))
    print(str(avg))
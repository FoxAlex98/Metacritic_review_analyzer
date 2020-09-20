from game_details import *
from reviews_mc_scraper import *

game = get_game_details()

print("scanning review of " + game['game_name'])

for i in range(len(game['platforms'])):
    print("scanning " + game['platforms'][i])
    scrape_game_reviews(game['game_name'],game['platforms'][i])

print("finish")
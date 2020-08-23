docker stop mc_scraper

docker container rm mc_scraper

docker build .. --rm --tag tap:metacritic_scraper

docker run --name mc_scraper tap:metacritic_scraper

docker stop mc_scraper

docker container rm mc_scraper

docker build .. --rm --tag tap:metacritic_scraper

docker run -it --name mc_scraper --network metacriticreviewanalyzer_tap tap:metacritic_scraper

docker stop mc_spark

docker container rm mc_spark

docker build .. --rm --tag tap:metacritic_spark

docker run --name mc_spark --network metacriticreviewanalyzer_tap tap:metacritic_spark

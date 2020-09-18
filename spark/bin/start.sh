rm ../utils.zip
pushd ../code/utils/
ls
zip -r ../../utils.zip ./
popd

docker stop mc-spark

docker container rm mc-spark

docker build .. --rm --tag tap:metacritic-spark

docker run --name mc-spark --network metacriticreviewanalyzer_tap tap:metacritic-spark

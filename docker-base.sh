mkdir -p build
docker-compose run -u $(id -u):$(id -g) --rm --service-ports $dockercmd 
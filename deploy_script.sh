container=$(docker ps | grep -w apiparksamart | awk '{print $1}')
if [[ $container ]]
    then
        docker container stop $container
        docker container rm $container
fi
{
    docker image rm api-parksamart
} || {
    echo "Server does not contain api-parksamart image!"
}
docker build -t api-parksamart:latest .
docker run -d -p 81:5000 api-parksamart:latest

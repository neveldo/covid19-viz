# Covid-19 viz (France)

## Description

Vizualisation of Covid-19 data from France.

## Run app

Whith Makefile :

```
make run
```

Or manually :

```
# Delete previous running container
docker stop covid19viz_01;docker rm covid19viz_01;

# Build the docker image
docker build -f docker/Dockerfile -t neveldo/covid19viz:1.0 .

# Create a container from the image
docker create --name=covid19viz_01 --hostname=host01 neveldo/covid19viz:1.0

# Start the container
docker start covid19viz_01 -d

# Or create & run a container
docker run -d --name covid19viz_01 neveldo/covid19viz:1.0
```
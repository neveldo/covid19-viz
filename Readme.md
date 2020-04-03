# Covid-19 viz (France)

## Description

This application allows users to vizualize some key data of the evolution of Covid-19 pandemy for France at country and departments scale.
The data are automatically updated every day. The source is ["Santé publique France"](https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/#_) .

The app is available online here : [http://covid19.vincentbroute.fr/](http://covid19.vincentbroute.fr/)

<img src="https://raw.githubusercontent.com/neveldo/covid19-viz/master/static/images/twitter-image.png" width="500px" height="500px" />

## Run app

Whith Makefile :

Run Flask debug server : 
```
make run-dev
```

Run the app through uwsgi + nginx server :
```
make run-prod
```
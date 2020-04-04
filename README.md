# imdb
## Internet Movies DashBoard

My first Web App.
A simple Flask (with Dash) + Nginx + MongoDB application.

Ready for deployment through Docker Compose:

```$ docker-compose up -d --build```

The flag ```d``` is for running on background via docker daemon, and ```--build``` is for rebuilding the images.

After deployment, the app can be accessed through your browser:

``` https://localhost```

The dashboard is on /dash/ path, so:

```https://localhost/dash``` 

TODO:

- Connect flask with MongoDB.
- Work on the visualizations formatting.
- Add more visualizations.
- Add more movies.

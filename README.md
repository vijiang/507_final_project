
# SI 507: Final Project

### Vivian Jiang

## About
This project requests data about Caribou's playlist, *[The Longest Mixtape: 1000 Songs for You](https://open.spotify.com/playlist/4Dg0J0ICj9kKTGDyFu0Cv4?si=K8WGBb1YQambb0X-IqK5xQ)*, from Spotify, via their API, and stores those tracks in a database using SQLAlchemy. Users will be able to check to see if certain songs or artists are in that playlist by entering a title or artist name as part of a Flask route: if a song is in the playlist, the application will also return Pitchfork’s rating of the album the song is present on, if available; If an artist is in the playlist, the application will return the song(s) present by the artist.

## Routes

-   Route 1: /instructions →
-   Route 2: /check/song/< trackname > →
-   Route 3: /check/artist/< artistname > →

## Notes & Assumptions

In order to simplify the relationships between entities in the database, we can assume the following rules:
1. Any single track will have only one album associated with it.
2. Any single album can have many tracks associated with it. 
3. Any single album will only have one review associated with it.

Please also note that, although the Spotify US indicates there are 924 tracks in the playlist, data from their API returns 1,012 tracks. I believe this is because some songs may be region-locked, and are therefore not available or able to be counted by the Spotify US interface.

In this project, I will be relying the **1,012** tracks returned by the API request.

## How to run the application
In your command line interface, navigate to the location of the project folder. Run the program by entering
```
python SI507project_tools.py
```
Thank you!
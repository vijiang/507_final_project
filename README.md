# SI 507 Final Project

Vivian Jiang
Link to this repository: [https://github.com/vijiang/507_final_project](https://github.com/vijiang/507_final_project)

---

## Project Description

This project requests data about Caribou's playlist, *[The Longest Mixtape: 1000 Songs for You](https://open.spotify.com/playlist/4Dg0J0ICj9kKTGDyFu0Cv4?si=K8WGBb1YQambb0X-IqK5xQ)*, from Spotify, via their API, and stores those tracks in a database using SQLAlchemy. Users will be able to check to see if certain songs or artists are in that playlist by entering a title or artist name as part of a Flask route: if a song is in the playlist, the application will also return Pitchfork’s rating of the album the song is present on, if available; If an artist is in the playlist, the application will return the song(s) present by the artist.

## How to run

1. First, you should navigate to the project folder.
2. Install all requirements via 
`pip install -r requirements.txt`
4. Run the program by entering
`python SI507project_tools.py`

## How to use

1. A useful instruction goes here
2. A useful second step here

Notes:

In order to simplify the relationships between entities in the database, we can assume the following rules:
1. Any single track will have only one album associated with it.
2. Any single album can have many tracks associated with it. 
3. Any single album will only have one review associated with it.

Please also note that, although the Spotify US indicates there are 924 tracks in the playlist, data from their API returns 1,012 tracks. I believe this is because some songs may be region-locked, and are therefore not available or able to be counted by the Spotify US interface.

In this project, I will be relying the **1,012** tracks returned by the API request.

Resources used: 
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - web scraping tool
- [Spotipy](https://spotipy.readthedocs.io/en/latest/) - Python library supporting the Spotify Web API
- nsgrantham's [Github repository](https://github.com/nsgrantham/pitchfork-reviews) with some pre-scraped Pitchfork data

## Routes in this application

-   Route 1: `/instructions` → shows you a greeting + gives instructions on how to user should enter information
-   Route 2: `/check/song/<trackname>` → checks if a certain track exists in the database/playlist
-   Route 3: `/check/artist/<artistname>` → checks if tracks by a given artist exist in the database/playlist

## How to run tests

1. First, navigate to the project folder
2. Second, run the specific test file: *SI507project_tests.py*

## In this repository:
[.gitignore](https://github.com/vijiang/507_final_project/blob/master/.gitignore ".gitignore")

[README.md](https://github.com/vijiang/507_final_project/blob/master/README.md "README.md")

[SI507project_tools.py](https://github.com/vijiang/507_final_project/blob/master/SI507project_tools.py "SI507project_tools.py")

[albums.json](https://github.com/vijiang/507_final_project/blob/master/albums.json "albums.json")

[caribou_playlist.db](https://github.com/vijiang/507_final_project/blob/master/caribou_playlist.db "caribou_playlist.db")

[caribou_tracks.json](https://github.com/vijiang/507_final_project/blob/master/caribou_tracks.json "caribou_tracks.json")

[draft_of_db_diagram.jpg](https://github.com/vijiang/507_final_project/blob/master/draft_of_db_diagram.jpg "draft_of_db_diagram.jpg")

[finalproject_tests.py](https://github.com/vijiang/507_final_project/blob/master/finalproject_tests.py "finalproject_tests.py")

[pitchfork-reviews.db](https://github.com/vijiang/507_final_project/blob/master/pitchfork-reviews.db "pitchfork-reviews.db")

---

## Code Requirements for Grading

### General

- [x] Project is submitted as a Github repository

- [ ] Project includes a working Flask application that runs locally on a

computer

- [ ] Project includes at least 1 test suite file with reasonable tests in it.

- [ ] Includes a `requirements.txt` file containing all required modules to run program

- [x] Includes a clear and readable README.md that follows this template

- [x] Includes a sample .sqlite/.db file

- [x] Includes a diagram of your database schema

- [x] Includes EVERY file needed in order to run the project

- [ ] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application

- [x] Includes at least 3 different routes

- [ ] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course

- [x] Interactions with a database that has at least 2 tables

- [x] At least 1 relationship between 2 tables in database

- [x] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)

- [x] Use of a new module

- [ ] Use of a second new module

- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)

- [ ] A many-to-many relationship in your database structure

- [ ] At least one form in your Flask application

- [ ] Templating in your Flask application

- [ ] Inclusion of JavaScript files in the application

- [ ] Links in the views of Flask application page/s

- [ ] Relevant use of `itertools` and/or `collections`

- [x] Sourcing of data using web scraping

- [x] Sourcing of data using web REST API requests

- [x] Sourcing of data using user input and/or a downloaded .csv or .json dataset

- [x] Caching of data you continually retrieve from the internet in some way

### Submission

- [ ] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)

- [ ] I included a summary of my project and how I thought it went **in my Canvas submission**!

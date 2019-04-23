import spotipy
import os
import json
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, session, redirect, url_for
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from advanced_expiry_caching_fp import Cache


# # ------ opening downloaded database table / originally by nsgrantham
# # https://github.com/nsgrantham/pitchfork-reviews

with open("albums.json", "r") as usefile:
    p4k_database = json.load(usefile)
    
# # ------ Setting up SQLAlchemy stuff/SQL table ------

# # from project planning doc:
# # I expect my database schema to include 3 tables. The entities each table will represent are: Playlist tracks, albums, and Pitchfork album reviews. There will be a many-to-one relationship between playlist tracks and the album table there will be a one-to-one relationship between the albums table and the Pitchfork reviews table.

app = Flask(__name__)
app.use_reloader = True

app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./caribou_playlist.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # For database use
session = db.session  # to make queries easy

class Tracks(db.Model):
    __tablename__= "playlist tracks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    album_name = db.relationship("Albums", backref = db.backref("name", lazy="dynamic"))

# # many-to-one relationship 

class Albums(db.Model):
    __tablename__= "albums"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.String)
    year = db.Column(db.String)
    label = db.Column(db.String)
    author = db.Column(db.String)
    url = db.Column(db.String)
    blurb = db.Column(db.String)

# one-to-one relationship

# class Reviews(db.Model):
#     __tablename__= "pitchfork reviews"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
#     r_album = db.relationship("Albums", backref = db.backref("pitchfork reviews", uselist=False))
#     album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    
#     author = db.Column(db.String(100), nullable=False)
#     rating = db.Column(db.Float(2), nullable=False)
#     description = db.Column(db.String(200))

# # ------ Setting up Spotify requests ------

SPOTIFY_CLIENT_ID = "fc28786916ef479b977f7dabacfb68ab"
SPOTIFY_SECRET = "764343631291468c9829c0274616b5f4"
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

username = "cariboutheband"
playlist_id = "4Dg0J0ICj9kKTGDyFu0Cv4"

results = {}

# # ------ Creating a simple cache of my data so I don't get blocked ------
try:
    cache = open("caribou_tracks", 'r')
    results = json.load(cache)
except FileNotFoundError:
    with open("caribou_tracks.json", 'w') as outfile:
        results = sp.user_playlist(username, playlist_id)
        tracks_info = results['tracks']
        tracks = tracks_info['items']
        while tracks_info['next']:
            tracks_info = sp.next(tracks_info)
            tracks.extend(tracks_info['items'])
        results['tracks']['items'] = tracks
        json.dump(results, outfile, indent=4)

# ------ Formatting data for the database/making it readable ------

def get_or_create_album(album_name, artist_name):
    album = Albums.query.filter_by(a_name=album_name).first()
    if album:
        # print("return A") checking which statement is passing
        return album
    else:
        album = get_info(album_name, artist_name)
        # print("return B") checking which statement is passing
        session.add(album)
        session.commit()
        # album = Albums.query.filter_by(a_name=album_name).first()
        return album

#  ------ using the pre-created database to search for album ratings
# this function does NOT commit or add anything to the database

def get_info(album_name, artist_name):
    lower_album=album_name.lower()
    lower_artist=artist_name.lower()
    for entry in p4k_database:
        if entry["album"].lower() == lower_album and entry["artist"].lower() == lower_artist:
            a_score = entry["score"]
            a_year = entry["released"]
            a_label = entry["label"]
            a_author = entry["reviewer"]
            a_url = entry["url"]
            try:
                abs_text = get_abstract(a_url)
            except:
                abs_text = "None"
            album = Albums(a_name=album_name, score = a_score, year = a_year, label = a_label, author = a_author, url = a_url, blurb = abs_text)
            return album
    
    return Albums(a_name=album_name, score="Not available!", year="Not available!", label="Not available!", author="Not available!", url="Not available!", blurb="Not available!")
       

def create_track():
    for song in results["tracks"]["items"]:
        s_album = song["track"]["album"]["name"]
        s_artist = song["track"]["artists"][0]["name"]
        s_title = song["track"]["name"]
        album = get_or_create_album(s_album, s_artist)
        track = Tracks(name=s_title, artist=s_artist, album_name=album)
        session.add(track)
        session.commit()
    return None


# ------ grabbing the review page url from the p4k db and scraping for blurb

# START_URL = "https://pitchfork.com/reviews/albums/"
FILENAME = "page_review_text.json"
PROGRAM_CACHE = Cache(FILENAME)

def access_page_data(url):
    data = PROGRAM_CACHE.get(url)  # get data associated with that identifier
    # unique identifier is the URL where the data lives
    # get will return none or false if the url does not exist
    if not data:
        # get the stuff that lives in that place is there is currently nothing there
        data = requests.get(url).text
        # default here with the Cache.set tool is that it will expire in 7 days, which is probs fine, but something to explore
        PROGRAM_CACHE.set(url, data)
        # url is identifier; data is what you want to associate with identifier
    return data

def get_abstract(url):  
    review_page = access_page_data(url)
    main_soup = BeautifulSoup(review_page, features="html.parser") # might move this out later
    abstract = main_soup.find("div", {"class": "review-detail__abstract"})
    return abstract.text


# ------ searching the "playlist tracks" entity table or a track or artist

def search_for_track(track_name):
    track = Tracks.query.filter_by(name=track_name).first()
    if track:
        return track
    else:
        return False

def search_for_artist(artist_name):
    tracks = Tracks.query.filter_by(artist=artist_name).all()
    if len(tracks):
        return tracks
    else:
        return False


# ------ Flask routes

@app.route('/<name>')
def index_route(name):
    visitor = name
    return render_template('index_template.html', name=visitor)

@app.route('/check/song/<title>')
def check_song(title):
    track = search_for_track(title) # this returns an instance of Tracks
    if track:
       album = track.album_name # this returns the album instance that is associated with the given track; contains all album info
       return "{} by {}, from the album {}, is in this playlist. The album was released in {} on the label {}. It has a rating of {} on Pitchfork. {} wrote the review. Here is the opening blurb to the article: {}. Read the full review here: {}".format(track.name, track.artist, album.a_name, album.year, album.label, album.score, album.author, album.blurb, album.url)
    else:
        return "{} was not found in this playlist. Maybe try another song?".format(title)

@app.route('/check/artist/<artistname>')
def check_artist(artistname):
    tracks = search_for_artist(artistname)
    if tracks:
        tracklist = []
        for song in tracks:
            tracklist.append(song.name)
        return "There are {} song(s) by {} in this playlist: {}.".format(len(tracklist), artistname, ", ".join(tracklist))
    else:
        return "There doesn't seem to be any songs by {} in this playlist. Try another artist?".format(artistname)


# ------ Making the program run

if __name__ == "__main__":
    db.create_all()
    create_track()
    app.run()

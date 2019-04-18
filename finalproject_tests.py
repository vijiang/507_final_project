import unittest
import json
from SI507project_tools import *
from flask_sqlalchemy import sqlalchemy


class hope_these_pass(unittest.TestCase):

    def test_retrived_playlist(self):
        self.assertEqual(results["tracks"]["total"], 1012, "Testing that there are 1,012 tracks in the playlist that is retrieved.")
        
        self.assertEqual(results["id"], playlist_id, "Testing that the playlist retrived has the same ID # as the playlist I intended to grab.")

    def test_db_creation(self):
        ## really not sure how to connect my test file to my SQLAlchemy database????
        # want to check that the length of the playlist tracks table is no longer than the total # of tracks returned from the API
        return None

    def test_get_create_album(self):
        self.assertIsInstance(get_or_create_album("Unknown Pleasures"), Albums, "testing that the return value is an instance of class Albums")

    def test_tracks_artists_albums(self):
        self.assertTrue(search_for_track("1 Thing"), "testing that 1 thing by amerie is in the playlist")

        self.assertTrue(search_for_artist("Joni Mitchell"), "testing that the database includes songs by joni mitchell")

        self.assertEqual(get_info("L oser"), "Album not found!",
                        "testing to make sure the program cannot find this album misspelling in the playlist")

    # def test_scraping(self): # this should work once i fix my actual code
    #     weyes_blood = "Natalie Mering’s fourth album is a grand, sentimental ode to living and loving in the shadow of doom. It is her most ambitious and complex work yet."
        
    #     self.assertIsInstance(get_abstract(
    #         "https://pitchfork.com/reviews/albums/weyes-blood-titanic-rising/"),weyes_blood, "testing if my scraping function is retrieving the right string from a page")

if __name__ == "__main__":
    unittest.main(verbosity=2)

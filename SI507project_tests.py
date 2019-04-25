import unittest
import json
from SI507project_tools import *
from flask_sqlalchemy import sqlalchemy


class hope_these_pass(unittest.TestCase):

    def test_retrived_playlist(self):
        self.assertEqual(results["tracks"]["total"], 1012, "Testing that there are 1,012 tracks in the playlist that is retrieved.")
        
        self.assertEqual(results["id"], playlist_id, "Testing that the playlist retrived has the same ID # as the playlist I intended to grab.")

    def test_get_create_album(self):
        self.assertIsInstance(get_or_create_album("Unknown Pleasures", "Joy Division"), Albums, "testing that the return value is an instance of class Albums")

    def test_tracks_artists_albums(self):
        self.assertTrue(search_for_track("1 Thing"), "testing that 1 thing by amerie is in the playlist")

        self.assertTrue(search_for_artist("Joni Mitchell"), "testing that the database includes songs by joni mitchell")

    def test_unavailable_review(self):
        test_album = get_info("Selected Ambient Works Volume II", "Aphex Twin")
        self.assertEqual(test_album.year, "Not available!", "testing that there is no review information available for this aphex twin album")


if __name__ == "__main__":
    unittest.main(verbosity=2)

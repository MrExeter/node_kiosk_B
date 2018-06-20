'''
Description - Utility class for creating, updating and deleting playlist directories and the respective symlinks contained
              within them.
@author - John Sentz
@date - 19-Jun-2018
@time - 8:55 PM
'''

import glob
import os

PLAYLIST_ROOT_DIRECTORY = "/home/pi/node_kiosk_B/app/static/videos/playlists/"


class LinkController(object):

    def create_playlist_directory(self, directory_name):
        directory = PLAYLIST_ROOT_DIRECTORY + directory_name

        try:
            if not os.path.isdir(directory):
                os.mkdir(directory_name)
        except OSError as e:
            print(e)

    def create_links(self, directory_path, *movie_links):
        movie_links = movie_links
        for movie_link in movie_links:
            os.symlink(movie_link[0].location, movie_link[1].full_filepath)
            dummy = 1

    def delete_links(self, directory_name):
        directory_path = PLAYLIST_ROOT_DIRECTORY + directory_name + "/*"
        files = glob.glob(directory_path)
        for f in files:
            os.remove(f)

    def delete_playlist_directory(self, directory_name):
        directory = PLAYLIST_ROOT_DIRECTORY + directory_name
        if os.path.exists(directory):
            # shutil.rmtree(directory_name)
            os.rmdir(directory)


'''
Description - System monitor utilities
@author - John Sentz
@date - 13-Mar-2018
@time - 5:31 PM
'''

import os
import subprocess

import psutil
from flask import jsonify

from app import db
from app.movie.models import Movie, Playlist


class SystemMonitor:
    cpu_temp = 0
    cpu_utilization = None
    up_time = {}
    memory_stats = {}
    disk_stats = {}
    json_data = {}

    def __init__(self):
        ###############################################################################
        # Return CPU temperature as a character string
        cpu_temp = float(os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline())
        cpu_temp = float(cpu_temp / 1000.)
        cpu_temp = str(round(cpu_temp, 1))      # + " C"

        cpu_utilization = str(psutil.cpu_percent()) + '%'

        ###############################################################################
        # Pull uptime in seconds
        # Days
        seconds = float(os.popen("awk '{print $1}' /proc/uptime").readline())
        days = int(seconds // (24 * 3600))

        ###############################################################################
        # Hours
        seconds = seconds % (24 * 3600)
        hours = int(seconds // 3600)

        ###############################################################################
        # Minutes
        seconds %= 3600
        minutes = int(seconds // 60)

        ###############################################################################
        # Seconds
        seconds %= 60
        seconds = int(seconds)

        ###############################################################################
        #
        # Build uptime stats dictionary
        #
        uptime_stats = {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }

        ###############################################################################
        # Memory calculation
        memory = psutil.virtual_memory()
        # Divide from Bytes -> KB -> MB
        memory_available = str(round(memory.available / 1024.0 / 1024.0, 1)) + " MB"
        memory_total = str(round(memory.total / 1024.0 / 1024.0, 1)) + " MB"
        memory_used_percent = str(memory.percent) + "%"

        ###############################################################################
        #
        # Build memory stats dictionary
        #
        memory_stats = {
            "memory_total": memory_total,
            "memory_available": memory_available,
            "memory_used_percent": memory_used_percent
        }

        ###############################################################################
        # Disk stats
        disk = psutil.disk_usage('/')
        # Divide from Bytes -> KB -> MB -> GB
        disk_free = str(round(disk.free / 1024.0 / 1024.0 / 1024.0, 1)) + " GB"
        disk_total = str(round(disk.total / 1024.0 / 1024.0 / 1024.0, 1)) + " GB"
        disk_used_percent = str(disk.percent) + "%"

        ###############################################################################
        #
        # Build disk stats dictionary
        #
        disk_stats = {
            "disk_total": disk_total,
            "disk_free": disk_free,
            "disk_used_percent": disk_used_percent
        }

        ###############################################################################
        #
        # Build Movie dictionary
        #
        movie_output = []
        movies = Movie.query.all()
        for movie in movies:
            movie_data = {}
            movie_data["id"] = movie.id
            movie_data["name"] = movie.name
            movie_data["file"] = movie.file_name
            movie_data["play_count"] = movie.play_count
            movie_data["currently_playing"] = str(movie.currently_playing)
            movie_data["play_on_start"] = str(movie.play_on_start)
            movie_output.append(movie_data)

        movie_output = sorted(movie_output, key=lambda i: i['id'], reverse=False)

        ###############################################################################
        #
        # Build Playlist dictionary
        #
        playlist_output = []
        playlists = Playlist.query.all()
        for playlist in playlists:
            playlist_data = {}
            playlist_data["id"] = playlist.id
            playlist_data["name"] = playlist.name
            playlist_data["directory_path"] = playlist.directory_path
            playlist_data["currently_playing"] = str(playlist.currently_playing)
            playlist_data["play_on_start"] = str(playlist.play_on_start)
            playlist_output.append(playlist_data)

        playlist_output = sorted(playlist_output, key=lambda i: i['id'], reverse=False)

        ###############################################################################
        #
        # Build Status dictionary
        #
        self.json_data = {
            "system": {
                "cpu_temp": cpu_temp,
                "cpu_utilization": cpu_utilization,
                "memory_stats": memory_stats,
                "disk_stats": disk_stats,
                "uptime": uptime_stats},

            "movie_data": movie_output,
            "playlist_data": playlist_output,
            "display_status": self.get_tv_status()
        }

    def __repr__(self):
        return "Hello Dingus"

    def get_system_stats(self):
        return jsonify(self.json_data)

    def get_tv_status(self):
        return SystemMonitor.get_display_status()

    @classmethod
    def get_display_status(cls):
        """ Read status text file that has one of three possible states
            On -- Monitor connected and turned on
            Standby -- Monitor connected but in standby
            ERROR -- Monitor error state, The HDMI cable likely not connected or damaged
        """
        file = "/home/pi/node_kiosk_B/app/utils/display_status.txt"
        lines = tuple(open(file, 'r'))      # Open display status file
        lines = ''.join(lines).rstrip()     # Convert to string and strip newline character

        if lines == 'On':
            return 'On'
        elif lines == 'Standby':
            return 'Standby'
        else:
            return 'ERROR'

    # @classmethod
    # def start_display_monitor(cls):
    #     """
    #         Launch bash script that continuously monitors the state of the display monitor, the script
    #         writes and updates to the display_status.txt file
    #     """
    #     cmd = "/home/pi/node_kiosk_B/app/utils/display_status.sh"
    #     process = subprocess.Popen(['/bin/bash', '-c', cmd])
    #     return process.pid

###############################################################################
#
# Kill, Loop, single play and playlist loop commands
#
###############################################################################
kill_command_single_video = 'sudo killall omxplayer.bin'
loop_command = 'omxplayer --no-osd -o local --loop --aspect-mode stretch '
single_play_command = 'omxplayer --no-osd -o local --aspect-mode stretch '
playlist_command = 'omxplayer --no-osd -o local --aspect-mode stretch '
#
###############################################################################


class BobUecker(object):

    # Class variable to store PID of playlist looping script
    PLAYSCRIPT_PID = None

    @classmethod
    def all_not_playing(cls):
        ###############################################################################
        #
        # Query the database and set all movies and playlists to not currently playing
        #
        movies = Movie.query.all()
        for movie in movies:
            movie.currently_playing = False

        playlists = Playlist.query.all()
        for playlist in playlists:
            playlist.currently_playing = False

        db.session.commit()
        return ''

    # @classmethod
    # def play_single(cls, video_id):
    #     movie = Movie.query.get(video_id)
    #
    #     BobUecker.all_not_playing()
    #     full_file_path = movie.location
    #     # command = single_play_command + full_file_path
    #     # BobUecker.stop_video()
    #     # process = subprocess.Popen([command],
    #     #                            shell=True,
    #     #                            stdin=None,
    #     #                            stdout=None,
    #     #                            stderr=None,
    #     #                            close_fds=True)
    #     # message = process.poll()
    #     # process_pid = process.pid
    #
    #     ################################################################################################
    #     # Debug, trying to locate D-bus
    #     player = OMXPlayer(full_file_path, args=['--no-osd', '--no-keys', '-b', '--vol -600'])
    #     print("Filename is {} ".format(player.get_filename()))
    #     # session["the_omxplayer"] = temp_omxplayer
    #
    #     ################################################################################################
    #     #
    #     # if process_pid and not message:
    #     #     # if subprocess has a pid and no return code, assume subprocess launched and set movie to playing
    #     #     movie.currently_playing = True
    #     #     db.session.commit()
    #     player.play()
    #     sleep(15)
    #     # player.pause()
    #
    #     return player

    @classmethod
    def loop_video(cls, video_id):
        """
        Take video_id, find video in database, retrieve full filepath, launch script that
        loops a single video as subprocess
        :param video_id:
        :return:
        """

        ###############################################################################
        #
        # Retrieve movie by ID and set all to not playing
        #
        movie = Movie.query.get(video_id)
        BobUecker.all_not_playing()

        full_file_path = movie.location
        command = loop_command + full_file_path

        ###############################################################################
        #
        # Kill playlist script if running, kill video player if running
        #
        BobUecker.stop_playlist()
        BobUecker.stop_video()

        cmd = "/home/pi/node_kiosk_B/app/utils/video_looper.sh" + " " + full_file_path
        process = subprocess.Popen(['/bin/bash', '-c', cmd])

        message = process.poll()
        BobUecker.PLAYSCRIPT_PID = process.pid
        output_str = "The process pid is : {}".format(BobUecker.PLAYSCRIPT_PID)

        ###############################################################################
        #
        # Set current movie to playing, save to database
        #
        movie.currently_playing = True
        db.session.commit()

        return None

    @classmethod
    def loop_playlist(cls, playlist_id):
        """
        Given a playlist_id, a playlist by that ID is retrieved from the database, the full file path is
        returned.  All videos and playlists are set to not playing, all playing videos and playlists are stopped.

        Then a playlist_looper.sh script is launched, The PID of that script is saved as a class variable.

        :param playlist_id:
        :return:
        """
        ###############################################################################
        #
        # Retrieve playlist by ID and set all to not playing
        #
        playlist = Playlist.query.get(playlist_id)
        directory_path = " " + playlist.directory_path

        ###############################################################################
        #
        # Kill playlist script if running, kill video player if running
        #
        BobUecker.all_not_playing()
        BobUecker.stop_playlist()
        BobUecker.stop_video()

        cmd = "/home/pi/node_kiosk_B/app/utils/playlist_looper.sh" + directory_path

        process = subprocess.Popen(['/bin/bash', '-c', cmd])

        message = process.poll()
        BobUecker.PLAYSCRIPT_PID = process.pid
        output_str = "The process pid is : {}".format(BobUecker.PLAYSCRIPT_PID)

        ###############################################################################
        #
        # Set current movie to playing, save to database
        #
        playlist.currently_playing = True
        db.session.commit()

        print(output_str)
        return output_str

    @classmethod
    def stop_playlist(cls):
        ###############################################################################
        #
        # Use PID to stop playlist script, then stop_video to terminate the video that is left playing
        #
        if BobUecker.PLAYSCRIPT_PID:
            kill_command_playlist = "sudo kill -SIGTERM " + str(BobUecker.PLAYSCRIPT_PID)
            os.system(kill_command_playlist)
            os.system(kill_command_single_video)
        return None

    @classmethod
    def stop_video(cls):
        if BobUecker.PLAYSCRIPT_PID:
            kill_command_playlist = "sudo kill -SIGTERM " + str(BobUecker.PLAYSCRIPT_PID)
            os.system(kill_command_playlist)
        os.system(kill_command_single_video)
        return None

    DISPLAY_WAKE_COMMAND = 'sudo echo on 0 | cec-client -s -d 1'
    DISPLAY_STANDBY_COMMAND = 'sudo echo standby 0 | cec-client -s -d 1'
    POWER_HDMI_ON_COMMAND = 'sudo tvservice -p'
    POWER_HDMI_OFF_COMMAND = 'sudo tvservice --off'

    @classmethod
    def wake_display(cls):
        ###############################################################################
        #
        # Launch display wakeup command
        #
        wake_cmd = 'sudo /home/pi/node_kiosk_B/app/utils/wakeup.sh'
        process = subprocess.Popen(wake_cmd,
                                   shell=True,
                                   stdin=None,
                                   stdout=None,
                                   stderr=None,
                                   close_fds=True)

    @classmethod
    def sleep_display(cls):
        ###############################################################################
        #
        # Launch display shutdown command
        #
        BobUecker.all_not_playing()
        BobUecker.stop_playlist()
        BobUecker.stop_video()

        sleep_cmd = 'sudo /home/pi/node_kiosk_B/app/utils/sleep_standby.sh'

        process = subprocess.Popen(sleep_cmd,
                                   shell=True,
                                   stdin=None,
                                   stdout=None,
                                   stderr=None,
                                   close_fds=True)

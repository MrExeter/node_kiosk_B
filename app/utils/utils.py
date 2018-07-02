'''
Description - System monitor utilities
@author - John Sentz
@date - 13-Mar-2018
@time - 5:31 PM
'''

import os
import subprocess
# System monitor using psutil
#
from time import sleep

import psutil
from flask import jsonify
from omxplayer.player import OMXPlayer

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
        # Return CPU temperature as a character string
        cpu_temp = float(os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline())
        cpu_temp = float(cpu_temp / 1000.)
        cpu_temp = str(round(cpu_temp, 1))      # + " C"

        cpu_utilization = str(psutil.cpu_percent()) + '%'

        # Pull uptime in seconds
        # Days
        seconds = float(os.popen("awk '{print $1}' /proc/uptime").readline())
        days = int(seconds // (24 * 3600))

        # Hours
        seconds = seconds % (24 * 3600)
        hours = int(seconds // 3600)

        # Minutes
        seconds %= 3600
        minutes = int(seconds // 60)

        # Seconds
        seconds %= 60
        seconds = int(seconds)

        uptime_stats = {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }

        # Memory calculation
        memory = psutil.virtual_memory()
        # Divide from Bytes -> KB -> MB
        memory_available = str(round(memory.available / 1024.0 / 1024.0, 1)) + " MB"
        memory_total = str(round(memory.total / 1024.0 / 1024.0, 1)) + " MB"
        memory_used_percent = str(memory.percent) + "%"
        memory_stats = {
            "memory_total": memory_total,
            "memory_available": memory_available,
            "memory_used_percent": memory_used_percent
        }

        # Disk stats
        disk = psutil.disk_usage('/')
        # Divide from Bytes -> KB -> MB -> GB
        disk_free = str(round(disk.free / 1024.0 / 1024.0 / 1024.0, 1)) + " GB"
        disk_total = str(round(disk.total / 1024.0 / 1024.0 / 1024.0, 1)) + " GB"
        disk_used_percent = str(disk.percent) + "%"
        disk_stats = {
            "disk_total": disk_total,
            "disk_free": disk_free,
            "disk_used_percent": disk_used_percent
        }

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

        self.json_data = {
            "system": {
                "cpu_temp": cpu_temp,
                "cpu_utilization": cpu_utilization,
                "memory_stats": memory_stats,
                "disk_stats": disk_stats,
                "uptime": uptime_stats},

            "movie_data": movie_output,
            "playlist_data": playlist_output
        }

    def __repr__(self):
        return "Hello Dingus"

    def get_system_stats(self):
        return jsonify(self.json_data)


kill_command_single_video = 'sudo killall omxplayer.bin'
loop_command = 'omxplayer --no-osd -o local --loop --aspect-mode stretch '
single_play_command = 'omxplayer --no-osd -o local --aspect-mode stretch '

playlist_command = 'omxplayer --no-osd -o local --aspect-mode stretch '


class BobUecker(object):

    # Class variable to store PID of playlist looping script
    PLAYSCRIPT_PID = None

    @classmethod
    def all_not_playing(cls):
        # Set all movies and playlists to not currently playing
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

        movie = Movie.query.get(video_id)

        BobUecker.all_not_playing()

        full_file_path = movie.location
        command = loop_command + full_file_path
        # os.system(kill_command_single_video)
        BobUecker.stop_playlist()
        BobUecker.stop_video()

        cmd = "/home/pi/node_kiosk_B/app/utils/video_looper.sh" + " " + full_file_path
        # cmd = "/home/pi/node_kiosk_B/app/utils/tester.sh" + directory_path

        process = subprocess.Popen(['/bin/bash', '-c', cmd])

        message = process.poll()
        BobUecker.PLAYSCRIPT_PID = process.pid
        output_str = "The process pid is : {}".format(BobUecker.PLAYSCRIPT_PID)

        movie.currently_playing = True
        db.session.commit()

        return None

    @classmethod
    def loop_playlist(cls, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        directory_path = " " + playlist.directory_path

        BobUecker.all_not_playing()
        BobUecker.stop_playlist()
        BobUecker.stop_video()

        cmd = "/home/pi/node_kiosk_B/app/utils/playlist_looper.sh" + directory_path
        # cmd = "/home/pi/node_kiosk_B/app/utils/tester.sh" + directory_path

        process = subprocess.Popen(['/bin/bash', '-c', cmd])

        message = process.poll()
        BobUecker.PLAYSCRIPT_PID = process.pid
        output_str = "The process pid is : {}".format(BobUecker.PLAYSCRIPT_PID)

        playlist.currently_playing = True
        db.session.commit()

        print(output_str)
        return output_str

    @classmethod
    def stop_playlist(cls):
        # Use PID to stop playlist script, then stop_video to terminate the video that is left playing
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

    DISPLAY_WAKE_COMMAND = 'echo on 0 | cec-client -s -d 1'
    DISPLAY_STANDBY_COMMAND = 'echo standby 0 | cec-client -s -d 1'

    @classmethod
    def wake_display(cls):
        os.system(BobUecker.DISPLAY_WAKE_COMMAND)

    @classmethod
    def sleep_display(cls):
        BobUecker.stop_video()
        os.system(BobUecker.DISPLAY_STANDBY_COMMAND)

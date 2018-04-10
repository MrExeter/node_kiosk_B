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
import psutil
from flask import jsonify

from app import db
from app.movie.models import Movie


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
            movie_output.append(movie_data)

        movie_output = sorted(movie_output, key=lambda i: i['id'], reverse=False)

        self.json_data = {
            "system": {
                "cpu_temp": cpu_temp,
                "cpu_utilization": cpu_utilization,
                "memory_stats": memory_stats,
                "disk_stats": disk_stats,
                "uptime": uptime_stats},

            "movie_data": movie_output
        }

    def __repr__(self):
        return "Hello Dingus"

    def get_system_stats(self):
        return jsonify(self.json_data)


kill_command = 'sudo killall omxplayer.bin'
loop_command = 'omxplayer -o local --loop --aspect-mode stretch '


class BobUecker(object):

    @classmethod
    def all_not_playing(cls):
        movies = Movie.query.all()
        for movie in movies:
            # Set all movies to not currently playing
            movie.currently_playing = False
            db.session.commit()

        return ''

    @classmethod
    def loop_video(cls, video_id):

        movie = Movie.query.get(video_id)

        BobUecker.all_not_playing()

        full_file_path = movie.location
        command = loop_command + full_file_path
        # os.system(kill_command)
        BobUecker.stop_video()
        process = subprocess.Popen([command],
                                   shell=True,
                                   stdin=None,
                                   stdout=None,
                                   stderr=None,
                                   close_fds=True)
        message = process.poll()
        process_pid = process.pid

        if process_pid and not message:
            # if subprocess has a pid and no return code, assume subprocess launched and set movie to playing
            movie.currently_playing = True
            db.session.commit()

        return None

    @classmethod
    def stop_video(cls):
        os.system(kill_command)
        return None



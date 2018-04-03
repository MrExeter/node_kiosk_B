# # System mon using psutil
# #
# import psutil
# import os
# from datetime import datetime, timedelta
# from flask import Flask, jsonify, Blueprint, request, session, redirect, url_for, render_template
# import time
# from time import sleep
# import subprocess
#
# from omxplayer.player import OMXPlayer
# from pathlib import Path
#
# app = Flask(__name__)
# app.debug = True  # Uncomment to debug
#
#
# # Return CPU temperature as a character string
# def get_cpu_temperature():
#     temp = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
#     return temp
#
#
# def get_up_time():
#     # Pull uptime in seconds
#     seconds = float(os.popen("awk '{print $1}' /proc/uptime").readline())
#     days = int(seconds // (24 * 3600))
#
#     seconds = seconds % (24 * 3600)
#     hours = int(seconds // 3600)
#
#     seconds %= 3600
#     minutes = int(seconds // 60)
#
#     seconds %= 60
#     seconds = int(seconds)
#
#     uptime_stats = {
#         "days": days,
#         "hours": hours,
#         "minutes": minutes,
#         "seconds": seconds
#     }
#
#     return uptime_stats
#
#
# def get_ram_info():
#     # Memory calculation
#     memory = psutil.virtual_memory()
#     # Divide from Bytes -> KB -> MB
#     memory_available = round(memory.available / 1024.0 / 1024.0, 1)
#     memory_total = round(memory.total / 1024.0 / 1024.0, 1)
#     memory_percent = str(memory.percent) + "%"
#     memory_stats = {
#         "memory_total": memory_total,
#         "memory_available": memory_available,
#         "memory_percent": memory_percent
#     }
#
#     return memory_stats
#
#
# def get_disk_info():
#     # Disk stats
#     disk = psutil.disk_usage('/')
#     # Divide from Bytes -> KB -> MB -> GB
#     disk_free = round(disk.free / 1024.0 / 1024.0 / 1024.0, 1)
#     disk_total = round(disk.total / 1024.0 / 1024.0 / 1024.0, 1)
#     disk_percent = str(disk.percent) + "%"
#     disk_stats = {
#         "disk_total": disk_total,
#         "disk_free": disk_free,
#         "disk_percent": disk_percent
#     }
#
#     return disk_stats
#
#
# @app.route('/')
# def home():
#     cpu_temp = float(get_cpu_temperature())
#     cpu_temp = float(cpu_temp / 1000.)
#     cpu_temp = str(round(cpu_temp, 1))
#     cpu_utilization = str(psutil.cpu_percent()) + '%'
#
#     memory_stats = get_ram_info()
#
#     disk_stats = get_disk_info()
#
#     # Get uptime
#     uptime = get_up_time()
#
#     json_data = {
#         "cpu_temp": cpu_temp,
#         "cpu_utilization": cpu_utilization,
#         "memory_stats": memory_stats,
#         "disk_stats": disk_stats,
#         "uptime": uptime
#     }
#
#     return jsonify(json_data)
#
#
# import logging
# logging.basicConfig(level=logging.INFO)
#
# VIDEO_PATH = Path("/home/pi/Videos/Iowa_Launch.mp4")
# dbus_name = 'org.mpris.MediaPlayer2.omxplayer1'
# player_log = logging.getLogger("Player 1")
#
# player = OMXPlayer(VIDEO_PATH,
#                    dbus_name='org.mpris.MediaPlayer2.omxplayer1')
#
#
# @app.route('/video/<int:command>')
# def play_video(command):
#
#     if command == 1:
#         player.play()
#
#     if command == 2:
#         player.pause()
#
#     if command == 3:
#         player.quit()
#
#     player.playEvent += lambda _: player_log.info("Play")
#     player.pauseEvent += lambda _: player_log.info("Pause")
#     player.stopEvent += lambda _: player_log.info("Stop")
#
#     return redirect(url_for('home'))
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
from flask_jwt import JWT
from flask_restful import Api

from app import create_app, db
from app.auth.models import User
from security import authenticate, identity

if __name__ == '__main__':
    flask_app = create_app('dev')

    # # JWT Authentication
    # api = Api(flask_app)
    # jwt = JWT(flask_app, authenticate, identity)  # generates endpoint /auth

    with flask_app.app_context():
        db.create_all()

        if not User.query.filter_by(user_name='napoleon').first():
            User.create_user(user='napoleon',
                             email='napoleon@dynamite.com',
                             password='applejack')

    flask_app.run(debug=True, host='0.0.0.0', port=5100)


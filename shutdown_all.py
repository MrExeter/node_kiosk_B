'''
Description - Shutdown class and script for shutting down all processes started in starter.py
@author - John Sentz
@date - 16-Oct-2018
@time - 11:08 AM
'''
import os
import subprocess


class APIShutdown:

    def __init__(self):
        pass

    @classmethod
    def shutdown_all(cls):

        #######################################################################
        # Shutdown Flask
        #
        flask_cmd = ['lsof', '-i', ':5000']
        try:
            return_str = subprocess.check_output(flask_cmd)
            return_str = return_str.split()
            print(return_str)
            #######################################################################
            # Every 10th element corresponds to a PID on port 5000
            #
            for pid in return_str[10::10]:
                print("Killing Flask server.....")
                os.system('kill ' + pid)
        except subprocess.CalledProcessError:
            print("Nothing found")

        #######################################################################
        # Shutdown display_status.sh
        #
        display_pids_cmd = ['pgrep', '-f', 'display_status']
        #######################################################################
        # display script might have multiple pids, collect all and kill
        #
        try:
            display_pids = subprocess.check_output(display_pids_cmd).split()
            for pid in display_pids:
                os.system('sudo kill -9 ' + pid)
        except subprocess.CalledProcessError:
            print("Display script shutdown.....")


APIShutdown.shutdown_all()
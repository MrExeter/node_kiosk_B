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
        flask_cmd = 'lsof -i :5000'
        try:
            return_str = subprocess.check_output(['lsof', '-i', ':5000'])
            return_str = return_str.split()
            print(return_str)
            for pid in return_str[10::10]:
                # the_PID = return_str[10]
                dummy = 99
                os.system('kill ' + pid)
        except subprocess.CalledProcessError:
            print("Nothing found")

        #######################################################################
        # Shutdown display_status.sh


APIShutdown.shutdown_all()
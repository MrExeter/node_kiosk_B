'''
Description - File and utility class to start flask app plus all support scripts.
@author - John Sentz
@date - 24-Sep-2018
@time - 8:32 PM
'''

import os
import subprocess
from time import sleep

import psutil

class Starter:

    FLASKAPP_UID = None
    DISPLAY_SCRIPT_UID = None

    @classmethod
    def clean_and_clear(cls):
        ###############################################################################
        #
        # look for and kill any occurrence of the Flask server running
        #
        flask_cmd = 'lsof -i :5000'
        try:
            return_str = subprocess.check_output(['lsof', '-i', ':5000'])
            return_str = return_str.split()
            print(return_str)
            the_PID = return_str[10]
            os.system('kill ' + the_PID)
        except subprocess.CalledProcessError:
            print("Nothing found")

        if Starter.DISPLAY_SCRIPT_UID is not None:
            os.system('kill ' + Starter.DISPLAY_SCRIPT_UID)

        else:
            print("Display script clear")

    @classmethod
    def start_all(cls):
        ###############################################################################
        #
        # launch display script and save UID of process
        #
        display_status_cmd = '/home/pi/node_kiosk_B/app/utils/display_status.sh'
        process = subprocess.Popen(display_status_cmd,
                                   shell=True,
                                   stdin=None,
                                   stdout=None,
                                   stderr=None,
                                   close_fds=True)
        script_pid = process.pid
        Starter.DISPLAY_SCRIPT_UID = script_pid
        print("The display script PID is : {}".format(script_pid))

        # launch flask server by by running run, save UID of process
        # launch_flask_cmd = ["python", "run.py"]
        launch_flask_cmd = "python run.py"
        process = subprocess.Popen(launch_flask_cmd,
                                   shell=True,
                                   stdin=None,
                                   stdout=None,
                                   stderr=None,
                                   close_fds=True)
        sleep(10)
        # process = subprocess.call(launch_flask_cmd)
        # process = subprocess.check_output(launch_flask_cmd)
        flask_pid = process.pid
        Starter.FLASKAPP_UID = flask_pid
        print("The Flask app is launched with PID : {}".format(Starter.FLASKAPP_UID))


# ###############################################################################
# #
# # Launch display wakeup command
# #
# flask_cmd = 'lsof -i :5000'
# # return_str = str(os.system(flask_cmd))
# try:
#     return_str = subprocess.check_output(['lsof', '-i', ':5000'])
#     dummy = 1
#     return_str = return_str.split()
#     print(return_str)
#     the_PID = return_str[10]
#     os.system('kill ' + the_PID)
# except subprocess.CalledProcessError:
#     print("Nothing found")
#
# # launch flask server by by running run, save UID of process
# launch_flask_cmd = ["python", "run.py"]
# # flask_process = subprocess.Popen(launch_flask_cmd, shell=True)
# os.system('python run.py')
# sleep(10)

# ##############################################################################
#
# # Launch display wakeup command
#
# display_status_cmd = '/home/pi/node_kiosk_B/app/utils/display_status.sh'
# process = subprocess.Popen(display_status_cmd)
# # process = subprocess.call(display_status_cmd, shell=True, close_fds=True)
#
# script_PID = process.pid
# print("The display script PID is : {}".format(script_PID))

Starter.clean_and_clear()
Starter.start_all()
sleep(15)
# process = subprocess.call(['python', 'hello_test.py'])

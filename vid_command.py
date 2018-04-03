from ffprobe import FFProbe
from omxplayer.player import OMXPlayer
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)

VIDEO_1_PATH = "app/static/videos/Iowa_Launch.mp4"

sleep(5)
player_log = logging.getLogger("Player 1")

player = OMXPlayer(VIDEO_1_PATH)
sleep(5)
player.play()
print
print "Player is playing : ", player.is_playing()
print "Player can play : ", player.can_play()



sleep(10)
player.quit()




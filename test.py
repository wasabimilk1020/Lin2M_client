import sys
import img_search_utils
import time
from button_func import *
import win32gui
from PIL import ImageGrab,ImageEnhance,Image,ImageOps,ImageFilter

result=img_search_utils.searchImg('game_start_2.png',beforeDelay=2, afterDelay=0,chkCnt=True, _region=(0,0,1920,1080))
print(result)




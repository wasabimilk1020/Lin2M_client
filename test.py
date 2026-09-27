import sys
import img_search_utils
import time
from button_func import *
import win32gui
from PIL import ImageGrab,ImageEnhance,Image,ImageOps,ImageFilter

x, y, width, height = 1270,330, 300, 300 #매칭 위치
match_list=["gift_1.png"]
match_result=img_search_utils.img_matchTemplate(match_list, x, y, width, height)
print("match_result",match_result)




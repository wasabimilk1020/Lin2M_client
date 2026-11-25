import sys
import img_search_utils
import time
from button_func import *
import win32gui
from PIL import ImageGrab,ImageEnhance,Image,ImageOps,ImageFilter
import serial_comm

# x, y, width, height = 1270,330, 300, 300 #매칭 위치
# match_list=["gift_1.png"]
# match_result=img_search_utils.img_matchTemplate(match_list, x, y, width, height,confidence=0.8)
# print("match_result",match_result)


# time.sleep(2)
# serial_comm.startClick(656,405,0,0,0)
result=img_search_utils.searchImg('confirm.png',beforeDelay=2, afterDelay=1, justChk=True, _region=(920,580,300,200))
print(result)
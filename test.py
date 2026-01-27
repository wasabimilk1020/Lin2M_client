import sys
import img_search_utils
import time
from button_func import *
import win32gui
from PIL import ImageGrab,ImageEnhance,Image,ImageOps,ImageFilter

for i in range(10):
  result=img_search_utils.img_matchTemplate(["auto_hunting.png","auto_organize.png","auto_schedule.png"], 805,670, 310, 50)
  time.sleep(0.3)
  print("결과",result)
# img_search_utils.preprocess_image("debug_capture_3.png", "preprocessed_3.png")

# img_search_utils.img_matchTemplate("auto_hunting.png", 895,220, 130, 35, confidence=0.8)
# time.sleep(2)
# hwnd = win32gui.GetForegroundWindow()
# rect = win32gui.GetWindowRect(hwnd)
# print(rect)

# x=805
# y=670
# width=255
# height=50
# bbox = (x, y, 1115, y + height)
# target_pil = ImageGrab.grab(bbox)

# # target_pil.show()
# target_pil.save("debug_capture_3.png")
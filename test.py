import sys
import img_search_utils
import time
from button_func import *
import win32gui
from PIL import ImageGrab,ImageEnhance,Image,ImageOps,ImageFilter

x,y=1295, 355 #초기 x,y좌표
for i in range(2):
  for j in range(4):
    print(i,j,x,y)
    x+=75
  x=1295 #x좌표 초기화
  y+=100
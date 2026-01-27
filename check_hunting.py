import img_search_utils
import time
import re

x, y, width, height = 805,670, 310, 50 #매칭 위치

match_list=["auto_hunting.png", "auto_organize.png", "auto_schedule.png"]
def checkHunting():
  for i in range(5):
    match_result=img_search_utils.img_matchTemplate(match_list, x, y, width, height)
    if match_result[0]==2:  #템플릿 매칭 예외 발생
      return match_result[0], match_result[1]
    elif match_result[0] in ["auto_hunting.png", "auto_organize.png", "auto_schedule.png"]: #매칭 성공
      return match_result[0].replace(".png", ""), ""
    time.sleep(0.3)
  return 0, "사냥 멈춰있음" #실패를 나타냄
import serial_comm
import check_hunting
import img_search_utils

ERR_MSG = 0
STATUS_MSG = 1

def go_to_sleep_and_huntingChk(btn_name, character_name, sio):
  for i in range(3):
    serial_comm.keyboard('g')
    result=img_search_utils.searchImg('sleepChk.png', beforeDelay=1, afterDelay=0,  chkCnt=2, _region=(850, 455, 200, 200))  
    if result ==1:
      break
  
  value=check_hunting.checkHunting()  #value=성공 시="자동 사냥 중" or "스케줄 자동 진행 중", 실패 시=0
  if value[0]==0: #0을 return (사냥을 하지 않고 있다는 뜻)
    sio.emit("logEvent",[f"{value[1]}", character_name, ERR_MSG])
  elif value[0]==2: #capture_text_from_region 예외 발생
    sio.emit("logEvent",[f"{value[1]}", character_name, STATUS_MSG])
  else:
    sio.emit("logEvent",[f"{btn_name}, {value[0]} 완료", character_name, STATUS_MSG])
import client_utils
import serial_comm
import time

def waking_from_sleep_and_deathChk(btn_name, sleep_time):
  if btn_name not in ["파티초대", "자동사냥"]:
    result=client_utils.searchImg('deathChk.png',beforeDelay=0, afterDelay=0, chkCnt=2, _region=(735,590,450,200))  #사망체크 "사망하였습니다"
  else:
    result=0
  
  #절전모드 해제 
  dragValues={'fromStartX':900, 'toStartX':1015,'fromStartY':590,'toStartY':620,'fromEndX':860, 'toEndX':1000,'fromEndY':325,'toEndY':345}
  serial_comm.mouseDrag(dragValues)
  time.sleep(sleep_time)   #실제로는 열렸는지 확인하는 코드 넣어야됨
  
  #페널티 클릭 루틴
  if result==1:
    client_utils.randClick(930,770,10,10,0)  
    chk_result=client_utils.searchImg('chk.png', beforeDelay=0, afterDelay=0, justChk=True, chkCnt=12, _region=(910,180,230,70))
    if chk_result==0:
      return result
  return 0
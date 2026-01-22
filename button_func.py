import time
import img_search_utils
from serial_comm import *
import re
import check_hunting
from waking_from_sleep import *
from go_to_sleep import *
import win32gui
import win32con

#data=[1142, 375, 10, 10, 0.0]=[x,y,xRange,yRange,delay]
def statusChk(sio, data, btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name
 
  value=check_hunting.checkHunting() #value=성공 시=문자열, 실패 시=0
  if value[0]==1: #1을 return (사냥을 하지 않고 있다는 뜻)
    result=waking_from_sleep_and_deathChk(btn_name, sleep_time=2)
    if result==1: #사망 체크를 수행 했는대 chk.png가 확인 안되서 실패
      return 0, "페널티 체크 루틴 실패"
    result=normalHunting(sio, data, btn_name, character_name, handle)
    return result
  elif value[0]==0: #capture_text_from_region 예외 발생
    return 1, value[1]
  else:  #성공
    text=value[0]
    return 2, text

def normalHunting(sio, data,btn_name, character_name, handle):
  coord=data
  flag=data[4]
  name=character_name

  if flag==1:
    keyboard('7')
    result_1=img_search_utils.searchImg('eventObj.png',beforeDelay=2, afterDelay=10, _region=(333,245,230,300)) 
    #여기에 클릭 후 확인이라던지 있는지 없는지 확인 하고 더 만들어줘야함함

  keyboard('v')

  img_search_utils.searchImg('stop_schedule.png',beforeDelay=0, afterDelay=0, chkCnt=2, _region=(1260,790,300,100))
  randClick(1075,820,10,10,1) #초기화 클릭

  result_1=img_search_utils.searchImg('memory_place.png',beforeDelay=0, afterDelay=1, _region=(320,400,200,150)) #기억장소 메뉴 클릭
  if(result_1==0):
    return 0, "기억장소 메뉴 실패"

  randClick(660,345,10,10,1)  #장소 클릭

  result_coord=img_search_utils.searchImg('plus.png',beforeDelay=0, afterDelay=0, justChk=True, _region=(1450,340,200,100)) #시간충전 좌표
 
  for i in range(7):
    randClick(result_coord[0],result_coord[1],0,0,0.3) #시간 충전

  result_2=img_search_utils.searchImg('clk_schedule_start.png',beforeDelay=0, afterDelay=0, _region=(1260,790,300,100))
  if result_2==1: #마을 체크
    result_village=img_search_utils.searchImg('portion.png',beforeDelay=0, afterDelay=0, chkCnt=30, justChk=True, _region=(340,245,200,300))
    if result_village!=0: #마을이면 5초 후 다음
      pass
      # time.sleep(5)
  else:
    return 0, "스케쥴 시작 실패"
    
  img_search_utils.caputure_image(name, 387, 258, sio) #name, x, y, sio
  
  return 1, "message:None"

def postBox(sio, data,btn_name, character_name, handle):
  keyboard(',')
  
  result=img_search_utils.searchImg('allAccept.png',beforeDelay=1, afterDelay=2)
  if(result==0):  
    return 0, "우편 모두받기 실패"

  img_search_utils.searchImg('confirm.png',beforeDelay=1, afterDelay=1, accuracy=0.9, _region=(920,580,300,200))

  escKey()  #우편 나가기
  
  return 1, "message:None"

#---------던전---------#
def dungeon(sio, data, btn_name, character_name, handle):
  coord=data
  charging=data[4]
  name=character_name
  
  if btn_name=="격전의섬":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    keyboard("`") #던전
    # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=img_search_utils.searchImg('dungeonG.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "격전의 섬 클릭 실패"

    result=img_search_utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기 
    if(result==0):
      return 0, "격섬 입장 클릭 실패"
    randClick(coord[0],coord[1],coord[2],coord[3],2)  #층 클릭

    keyboard('6') #순간이동

  elif btn_name=="파괴된성채":
    for i in range(charging):
      keyboard("1")
      time.sleep(2)

    keyboard("`") #던전
    result=img_search_utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=img_search_utils.searchImg('dungeonD.png',beforeDelay=0, afterDelay=1, chkCnt=10)
    if(result==0):
      print("파괴된 성채 실패")
      return 0, "파괴된성채 클릭 실패"

    result=img_search_utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=1, chkCnt=10, _region=(1200, 750, 400, 150))  #입장하기 
    if(result==0):
      return 0, "파괴성 입장 클릭 실패"
    randClick(coord[0],coord[1],coord[2],coord[3],2)  #층 클릭

    keyboard('6') #순간이동

  elif btn_name=="크루마탑":
    # for i in range(charging):
    #   keyboard("1")
    #   time.sleep(2)
    keyboard("`") #던전
    result=img_search_utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=img_search_utils.searchImg('cruma.png',beforeDelay=0, afterDelay=1, chkCnt=10)
    if(result==0):
      return 0, "크루마탑 클릭 실패"

    result=img_search_utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기
    if(result==0):
      return 0, "크루마 입장 클릭 실패"
    randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭 

  elif btn_name=="안타라스":
    print(f"{btn_name} 실행") #임시
  
    # for i in range(charging):
    #     keyboard("1")
    #     time.sleep(2)

    # keyboard("`") #던전
    # result=client_utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    # result=client_utils.searchImg('antaras.png',beforeDelay=1, afterDelay=1)
    # if(result==0):
    #   return 0, "안타라스 클릭 실패"

    # result=client_utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=0, _region=(1200, 750, 400, 150))  #입장하기
    # if(result==0):
    #   return 0, "안타 입장 클릭 실패"
    # # randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭 (설정 해줘야함 json에서)

  elif btn_name=="상아탑":
    for i in range(charging):
      keyboard("4")
      time.sleep(2)

    keyboard('v')
    img_search_utils.searchImg('stop_schedule.png',beforeDelay=0.5, afterDelay=0.5, _region=(1260,790,300,100))
    randClick(1075,820,10,10,0.5) #초기화 클릭

    result=img_search_utils.searchImg('sanga.png',beforeDelay=0.5, afterDelay=0.5, _region=(480, 455, 400, 300))
    if(result==0):
      return 0, "상아탑 클릭 실패"
    
    randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭 (설정 해줘야함 json에서)
    
    result_coord=img_search_utils.searchImg('plus.png',beforeDelay=0, afterDelay=0, justChk=True, _region=(1450,340,200,100)) #시간충전 좌표
 
    for i in range(7):
      randClick(result_coord[0],result_coord[1],0,0,0.3) #시간 충전
      
    result_3=img_search_utils.searchImg('clk_schedule_start.png',beforeDelay=0, afterDelay=0, _region=(1260,790,300,100))

  elif btn_name=="이벤트던전":
    print(f"{btn_name} 실행") #임시

    keyboard("`") #던전
    # result=client_utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=img_search_utils.searchImg('eventDun.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "이벤트던전 클릭 실패"

    result=img_search_utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=1, _region=(1200, 750, 400, 150))  #입장하기
    if(result==0):
      return 0, "이벤트 입장 클릭 실패"
    # randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭 (설정 해줘야함 json에서)
    randClick(1050,650,5,5,0)

    keyboard('6') #순간이동
  
  #이동 완료 체크
  result=img_search_utils.searchImg('chk.png', beforeDelay=1, afterDelay=1, justChk=True, chkCnt=10,_region=(910,180,230,70))
  if(result==0):
    return 0, f"{btn_name} 이동 실패"

  img_search_utils.caputure_image(name, 387, 258, sio) #name, x, y, sio

  return 1, "message:None"

#---------아이템 변경---------#
def switch_get_item(sio, data, btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정
  result=img_search_utils.searchImg('setting_get_btn.png', beforeDelay=1, afterDelay=1, _region=(355,370,200,200))
  if(result==0):
    return 0, "세팅 획득 버튼클릭 실패"
  
  if btn_name=="모두":
    result=img_search_utils.searchImg('allItem.png', beforeDelay=1, afterDelay=1, _region=(1210,360,200,150))
    if(result==0):
      return 0, "모두 클릭 실패"
    
    img_search_utils.caputure_image(name, 1295, 400, sio) #name, x, y, sio

  elif btn_name=="고급":
    result=img_search_utils.searchImg('greenItem.png', beforeDelay=1, afterDelay=1, _region=(1015,400,200,150))
    if(result==0):
      return 0, "고급 클릭 실패"
    
    img_search_utils.caputure_image(name, 1120, 450, sio) #name, x, y, sio

  elif btn_name=="희귀":
    result=img_search_utils.searchImg('blueItem.png', beforeDelay=1, afterDelay=1, _region=(1190,400,200,150))
    if(result==0):
      return 0, "희귀 클릭 실패"
    
    img_search_utils.caputure_image(name, 1280, 450, sio) #name, x, y, sio

  escKey()  #나가기
  return 1, "message:None"

def decomposeItem(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("0") #분해
  time.sleep(1)

  randClick(1480,735,5,5,1) #분해 목록
  randClick(1395,730,10,10,1) #분해 목록 확인
  randClick(1321,735,5,5,1) #분해

  img_search_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=1, chkCnt=2, _region=(920,580,300,200))
  
  img_search_utils.caputure_image(name, 1280, 340, sio) #name, x, y, sio

  return 1, "message:None"

def decomposeBook(sio, data,btn_name, character_name,handle):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("9") #분해
  time.sleep(1)

  randClick(1480,735,5,5,0.5) #분해 목록
  randClick(1395,730,10,10,0.5) #분해 목록 확인
  randClick(1321,735,5,5,0.5) #분해

  img_search_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=1, chkCnt=2, _region=(920,580,300,200))
  
  img_search_utils.caputure_image(name, 1280, 340, sio) #name, x, y, sio

  return 1, "message:None"
  
def deathChk(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name
  img_search_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=1, chkCnt=2, _region=(920,580,300,200))

  img_search_utils.caputure_image(name, 1145, 195, sio) #name, x, y, sio

  return 1, "message:None"

def showDiamond(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name

  keyboard('x')
  # Box(left=880, top=196, width=25, height=27)
  result_1=img_search_utils.searchImg('diamondChk_1.png', beforeDelay=1, afterDelay=0, justChk=True, _region=(840,180,100,60), accuracy=0.7)
  result_2=img_search_utils.searchImg('diamondChk_2.png', beforeDelay=0, afterDelay=0, justChk=True, _region=(920,180,80,60), accuracy=0.7)
  
  if result_1!=0 and result_2!=0:
    x=result_1.left+result_1.width
    capture_width=result_2.left-x #끝나는 x좌표는 고정정
    y, height = 190, 35 
    config="--psm 7 -c tessedit_char_whitelist=0123456789,"
    binary_val=150

    text=img_search_utils.capture_text_from_region(x, y, capture_width, height, config,binary_val)
    if text[0]==0:  #capture_text_from_region 예외 발생
      return 1, text[1] 
    numbers = ''.join(re.findall(r'\d+', re.sub(r"[.,]", "", text[0])))  #문자와 , . 제거 후 숫자만 남김
    diamond=numbers
  else:
    return 0, "다이아 이미지서치 실패"
  
  escKey()  #나가기

  return 3, diamond

def useItem(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name
  
  keyboard('i') #인벤토리
  time.sleep(1)
  randClick(1520,735,5,5,1) 
  randClick(1450,520,10,5,0.5)  #일괄사용 클릭

  randClick(1305,680,5,5,0.5)
 
  randClick(1405,740,5,5,10) 

  return 1, "message:None"

def agasion(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("i")
  time.sleep(1)
  randClick(1220,460,5,5,1) #왼쪽 메뉴 클릭

  while True:
    randClick(1290,505,5,5,0.5) #첫 번째 카드 클릭
    randClick(1290,505,5,5,0)
    result=img_search_utils.searchImg('agasionFirstChk.png', beforeDelay=1, afterDelay=1, justChk=True, _region=(800,750,300,200))
    if(result==0):
      break
    for j in range(30):
      keyboard("y")
      time.sleep(1)
      keyboard("y")
      result=img_search_utils.searchImg('agasionExit.png', beforeDelay=1, afterDelay=1, chkCnt=3,_region=(830,775,300,140))
      if(result==1):
        break

  return 1, "message:None"

def itemDelete(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name

  keyboard('v')
  img_search_utils.searchImg('stop_schedule.png',beforeDelay=1, afterDelay=0, chkCnt=2, _region=(1260,790,300,100))
  
  escKey()  #나가기

  keyboard("i")
  time.sleep(1)
  randClick(1225,405,5,5,1)

  randClick(1365,355,5,5,0.5) #순간이동
  randClick(1305,740,5,5,0.5)
  randClick(1030,705,5,5,0.5)
  randClick(1055,655,5,5,0.5)

  randClick(1295,355,5,5,0.5) #물약
  randClick(1305,740,5,5,0.5)
  randClick(1030,705,5,5,0.5)
  randClick(1055,655,5,5,2)

  randClick(1295,425,5,5,0.5) #초록물약
  randClick(1305,740,5,5,0.5)
  randClick(1030,705,5,5,0.5)
  randClick(1055,655,5,5,2)

  result=img_search_utils.searchImg('chk.png', beforeDelay=1, afterDelay=1, justChk=True, chkCnt=10,_region=(910,180,230,70))
  if(result==0):
    return 0, "아이템 삭제 실패"
  
  return 1, "message:None"

def paper(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name
  
  keyboard("i")
  time.sleep(1)
  randClick(1225,405,10,10,1)
  randClick(1439,355,10,10,0.5)
  randClick(1373,737,5,5,0.5)
  result=img_search_utils.searchImg('paper_make.png', beforeDelay=1, afterDelay=1, _region=(1255,488,200,100))
  if(result==0):
    return 0, "신탁서 제작 클릭 실패"

  randClick(1230,475,5,5,2)

  for i in range(6):
    randClick(630,345,10,10,0.5)
    randClick(1050,825,5,5,0.5) #max클릭
    randClick(1450,825,10,10,1) #제작클릭

    result=img_search_utils.searchImg('createCancel.png', beforeDelay=1, afterDelay=1, justChk=True, _region=(1340,765,300,200))
    if(result==0):
      break
    time.sleep(3)
    randClick(945,820,10,10,1)
    randClick(945,820,10,10,0.5)

  escKey()  #나가기
  
  return 1, "message:None"

def event_store(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name

  keyboard('7')
  
  result=img_search_utils.searchImg('event_store1.png', beforeDelay=1, afterDelay=3, chkCnt=10)  
  if(result==0):
    return 0, "이벤트상점 클릭 실패"
    
  result=img_search_utils.searchImg('dailyProduct.png', beforeDelay=1, afterDelay=1, chkCnt=30)  
  if(result==0):
    return 0, "일일상품담기 실패"
  
  # for i in range(8):
  #   randClick(490,465,10,10,0)

  randClick(1475,830,5,5,0.5) #구매 결정
  randClick(1050,650,5,5,0.5) 
  escKey()

  # result=client_utils.searchImg('event_store2.png', beforeDelay=1, afterDelay=3, chkCnt=10)  
  # if(result==0):
  #   return 0, "이벤트상점 클릭 실패"
    
  # result=client_utils.searchImg('dailyProduct.png', beforeDelay=1, afterDelay=1, chkCnt=30)  
  # if(result==0):
  #   return 0, "일일상품담기 실패"
  
  # # for i in range(8):
  # #   randClick(490,465,10,10,0)

  # randClick(1475,830,5,5,0) #구매 결정
  # randClick(1050,650,5,5,0) 
  # escKey()

  result=normalHunting(sio, data,btn_name, character_name, handle)
  return result

#거리 40M
def fourty(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정

  result=img_search_utils.searchImg('fourty_meter.png', beforeDelay=1, afterDelay=1, _region=(1065,710,550,200)) 
  if(result==0):
    return 0, "40M 클릭 실패"

  img_search_utils.caputure_image(name, 1300, 720, sio) #name, x, y, sio

  escKey()  #나가기

  return 1, "message:None"

#거리 제한없음
def unlimit(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정
  

  result=img_search_utils.searchImg('unlimit_meter.png', beforeDelay=1, afterDelay=1, _region=(1065,710,550,200)) 
  if(result==0):
    return 0, "제한없음 클릭 실패"

  img_search_utils.caputure_image(name, 1450,720, sio) #name, x, y, sio

  escKey()  #나가기

  return 1, "message:None"

#데일리 출석 루틴
def daily(sio, data,btn_name, character_name, handle):
  coord=data
  list_cnt=data[4]  #궁극적으로는 출석체크 목록갯수를 저절로 파악하게 만들어야된다.
  name=character_name

  keyboard(";") #출석

  #빨간색 점 없애는 루틴
  chk_y=320
  for i in range(list_cnt):
    randClick(1485,chk_y,10,10,0.5)
    chk_y+=80
  
  y = 255
  for i in range(list_cnt):
    region = (1530, y, 100, 70)
    
    result=img_search_utils.searchImg('dailyRedDotChk.png', beforeDelay=0, afterDelay=0, justChk=True, chkCnt=2, _region=region) 
    if result:
      randClick(result.left-100, result.top+30,10,10,1)
      result=img_search_utils.searchImg('accept.png', beforeDelay=1, afterDelay=1, _region=(1075,470,400,200)) 
      if(result==1):
        result=img_search_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=0, _region=(920,580,300,200)) 
   
    y += 80 #y축 80씩 증가
 
  #데일리 나가기
  escKey()

  return

#혈맹 출석 루틴
def guild(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name
  keyboard('.')

  result=img_search_utils.searchImg('guildAttendance.png', beforeDelay=1, afterDelay=1, accuracy=0.9,_region=(500,610,300,150)) 
  if(result==0):
    return 0, "혈맹 체크 실패"
  
  randClick(915, 820, 20, 20, 1)  #기부
  
  randClick(555,745,10,10,1)  #기본기부 받기
  
  escKey()  #기부 나가기
  escKey()  #혈맹 나가기

  return 1, "message:None"

def store(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name
  #상점 클릭
  keyboard('u')
  
  result=img_search_utils.searchImg('adChk.png', beforeDelay=5, afterDelay=1, _region=(235,665,350,235))  #광고 체크 
  #광고 없으면 그냥 진행 (예외처리 필요 없음)
  
  #교환소 클릭
  result=img_search_utils.searchImg('exchange.png', beforeDelay=0, afterDelay=1, _region=(340,210,1260,160))
  if(result==0):
    escKey()
    return 0, "교환소 클릭 실패"
  
  #품절 체크
  result=img_search_utils.searchImg('soldoutChk.png', beforeDelay=0, afterDelay=0, chkCnt=3, _region=(600,660,750,200))
  if(result==1):
    return 0, "솔드아웃"
  
  #일괄 구매
  result=img_search_utils.searchImg('allBuy.png', beforeDelay=0, afterDelay=1, _region=(1300,790,350,200))
  if(result==0):
    return 0, "일괄구매 실패"

  randClick(1045,780,10,10,3) #구매 클릭


  #---레아의 성소 클릭
  result=img_search_utils.searchImg('leah_castle.png', beforeDelay=1, afterDelay=1, accuracy=0.9, _region=(1360,370,200,100)) 
  #일괄 구매
  randClick(1442, 850, 100, 10, 0.5)
  #구매
  randClick(1039, 771, 100, 10, 2.5)

  # #---사제의 의뢰 시작
  # randClick(1405, 544, 100, 10, 0.5)
  # #일괄 구매
  # randClick(1442, 850, 100, 10, 1)
  # #구매
  # randClick(1039, 771, 100, 10, 2.5)

  #상점 나가기
  escKey()

  return 1, "message:None"

#------------모닝 루틴------------#
def morning(sio, data,btn_name, character_name, handle):
  coord=data
  delay=data[4]
  name=character_name

  # 데일리 
  daily(sio, data,btn_name, character_name, handle)
  # 혈맹 
  result_1=guild(sio, data,btn_name, character_name, handle)
  if(result_1[0]==0):
    return result_1[0], result_1[1]
  #상점
  result_2=store(sio, data,btn_name, character_name, handle)
  if(result_2[0]==0):
    return result_2[0], result_2[1]

  img_search_utils.caputure_image(name, 387,258, sio) #name, x, y, sio

  return 1, "message:None"

def seasonpass(sio, data,btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("z") #시즌패스
  time.sleep(2)

  x_coord=700
  for i in range(cnt):
    while(True):
      result=img_search_utils.searchImg('getSeason.png', beforeDelay=0, afterDelay=1,_region=(1110,330,350,150))
      if(result==0):
        randClick(1325,825,10,10,0)
        result=img_search_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=0, _region=(920,580,300,200))
        randClick(x_coord,280,30,10,1)
        break
    x_coord=x_coord+240
    
   
  img_search_utils.caputure_image(name, 1175,365, sio) #name, x, y, sio
  
  escKey()  #나가기

  return 1, "message:None"

def make_item(sio, data, btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("-") #제작
  time.sleep(2)

  result=img_search_utils.searchImg('armor.png', beforeDelay=0, afterDelay=1,_region=(475,215,500,150))
  if(result==0):
    return 0, "방어구 클릭 실패"
  
  result=img_search_utils.searchImg('half_plate.png', beforeDelay=0, afterDelay=1,_region=(480,270,400,300))
  if(result==0):
    return 0, "플레이트 클릭 실패"

  for i in range(cnt):
    randClick(1260,825,5,5,0.5)
  
  result=img_search_utils.searchImg('make.png', beforeDelay=0, afterDelay=6,_region=(1315,745,250,200))
  if(result==0):
    return 0, "제작 클릭 실패"
  
  result=img_search_utils.searchImg('white_confirm.png', beforeDelay=0, afterDelay=1, chkCnt=10, _region=(830,735,250,200))
  if(result==0):
    return 0, "제작 클릭 실패"
  
  escKey()  #나가기

  return 1, "message:None"

def party_dun_entry(sio, data,btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard('t') #파티설정
  result=img_search_utils.searchImg('party_dun_entry.png',beforeDelay=1, afterDelay=1, _region=(960, 755, 200, 100))
  if(result==0):
    randClick(950,795,5,5,0.5)

  return 1, "message:None"

def unparty(sio, data,btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  randClick(865,480,30,30,0.5)  #전리품 확인 클릭

  y=560
  keyboard("t") #파티
  for i in range(4):
    randClick(970,y,5,5,0)
    result=img_search_utils.searchImg('unparty.png',beforeDelay=0.5, afterDelay=0.5, _region=(980, 480, 300, 400))
    if(result==1):
      break
    y=y+60

  result=normalHunting(sio, data, btn_name, character_name, handle)
  return result

def party_dungeon(sio, data, btn_name, character_name, handle):
  coord=data
  charging=data[4]
  name=character_name

  keyboard("`") #던전
  # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭
  result=img_search_utils.searchImg('party.png',beforeDelay=1, afterDelay=0, _region=(630, 230, 400, 100))
  if(result==0):
    return 0, "파티클릭 실패"
  
  if btn_name=="봉인사원":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    result=img_search_utils.searchImg('sealing_temple.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "봉인의 사원 클릭 실패"

  elif btn_name=="카이트해적":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    result=img_search_utils.searchImg('kite_pirates.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "카이트해적 클릭 실패"
    
  elif btn_name=="네뷸라이트":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    result=img_search_utils.searchImg('nebul.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "네뷸라이트 클릭 실패"
    
  elif btn_name=="회색제단":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    dragValues={'fromStartX':680, 'toStartX':980,'fromStartY':650,'toStartY':750,'fromEndX':680, 'toEndX':980,'fromEndY':120,'toEndY':160}
    serial_comm.mouseDrag(dragValues)
    time.sleep(2)   

    result=img_search_utils.searchImg('gray_ash.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "회색제단 클릭 실패"
    
  elif btn_name=="최후정원":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    result=img_search_utils.searchImg('last_garden.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "최후정원 클릭 실패"
    
  elif btn_name=="케트라":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    dragValues={'fromStartX':680, 'toStartX':980,'fromStartY':650,'toStartY':750,'fromEndX':680, 'toEndX':980,'fromEndY':120,'toEndY':160}
    serial_comm.mouseDrag(dragValues)
    time.sleep(2)

    result=img_search_utils.searchImg('ketra.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "케트라 클릭 실패"

  result=img_search_utils.searchImg('request_enter.png', beforeDelay=0, afterDelay=1, _region=(1200, 750, 400, 150))  #입장신청
  if(result==0):
    return 0, f"{btn_name} 입장 클릭 실패"
  
  randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭
  result=img_search_utils.searchImg('confirm_enter.png', beforeDelay=0, afterDelay=1, _region=(880, 570, 320, 200))  #입장신청
  if(result==0):
    return 0, f"{btn_name} 입장신청 확인 실패"

  return 1, "message:None"

def go_home(sio, data, btn_name, character_name, handle):
  coord=data
  charging=data[4]
  name=character_name
  
  img_search_utils.caputure_image(name, 355, 410, sio) #name, x, y, sio

  keyboard('7') #귀환
  result=img_search_utils.searchImg('chk.png', beforeDelay=5, afterDelay=2, justChk=True, chkCnt=10,_region=(910,180,230,70))
  if(result==0):
    return 0, f"{btn_name} 이동 실패"
  
  keyboard('f') #자동사냥
  time.sleep(0.5)

  return 1, "message:None"


def class_add(sio, data, btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("l") #클래스 합성
  time.sleep(2)

  result=img_search_utils.searchImg('class_add.png', beforeDelay=0, afterDelay=3,_region=(360,240,700,100))
  if(result==0):
    return 0, "합성 클릭 실패"

  for i in range(cnt):
    keyboard("y")
    time.sleep(1)
  
  escKey()
  time.sleep(1)
  escKey()  #나가기

  return 1, "message:None"

def aga_add(sio, data, btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("q") #아가시온 합성
  time.sleep(2)

  result=img_search_utils.searchImg('class_add.png', beforeDelay=0, afterDelay=3,_region=(360,240,700,100))
  if(result==0):
    return 0, "합성 클릭 실패"

  for i in range(cnt):
    keyboard("y")
    time.sleep(1)
  
  escKey()
  time.sleep(1)
  escKey()  #나가기

  return 1, "message:None"

def item_exchange(sio, data, btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("n") #거래소

  result=img_search_utils.searchImg('add_sell.png', beforeDelay=2, afterDelay=1,_region=(530,255,600,100))
  if(result==0):
    return 0, "판매등록 실패"

  randClick(1363,338,10,10,1) #장비메뉴

  slot_x=1286
  for i in range(3):
    randClick(slot_x,408,10,10,0) #장비클릭
    result_1=img_search_utils.searchImg('low_sell_text.png', beforeDelay=0, afterDelay=0, justChk=True, _region=(965,460,300,100), accuracy=0.7)

    if result_1!=0:
      x, capture_width=1234, 50
      y, height = 486, 35 
      config="--psm 7 -c tessedit_char_whitelist=0123456789,"
      binary_val=150
    
      text=img_search_utils.capture_text_from_region(x, y, capture_width, height, config,binary_val)
      
      if text[0]==0:  #capture_text_from_region 예외 발생
        return 1, text[1] 
      numbers = ''.join(re.findall(r'\d+', re.sub(r"[.,]", "", text[0])))  #문자와 , . 제거 후 숫자만 남김
      if numbers=="10":
        randClick(1052,815,10,10,1) #확인 클릭
        randClick(1040,690,10,10,1) #등록 클릭
      else:
        escKey()
        slot_x=slot_x+77
    else:
      break
  escKey()  #나가기

  return 1, "message:None"

def re_exchange(sio, data, btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("n") #거래소

  result=img_search_utils.searchImg('add_sell.png', beforeDelay=2, afterDelay=2,_region=(530,255,600,100))
  if(result==0):
    return 0, "판매등록 실패"

  randClick(1125,833,10,10,0.5) #모두선택
  randClick(1447,833,10,10,0) #선택 재등록
  result=img_search_utils.searchImg('confirm.png',beforeDelay=0, afterDelay=1, _region=(920,580,300,200))
  if(result==1):
    time.sleep(15)
    
  escKey()  #나가기

  return 1, "message:None"

def get_exchange(sio, data, btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("n") #거래소
  time.sleep(2)

  randClick(777,275,10,10,1) #정산

  randClick(1450,835,10,10,0.5) #정산 확인
    
  escKey()  #나가기

  return 1, "message:None"

def magic_ink(sio, data, btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name

  #상점 클릭
  keyboard('u')
  
  result=img_search_utils.searchImg('adChk.png', beforeDelay=4, afterDelay=1, _region=(235,665,350,235))  #광고 체크 
  #광고 없으면 그냥 진행 (예외처리 필요 없음)

  #교환소 클릭
  result=img_search_utils.searchImg('exchange.png', beforeDelay=0, afterDelay=1, _region=(340,210,1260,160))
  if(result==0):
    escKey()
    return 0, "교환소 클릭 실패"
  
  randClick(1405,545,10,10,0) #사제의뢰 클릭

  result=img_search_utils.searchImg('ink.png', beforeDelay=0, afterDelay=1, _region=(355,655,1000,200))
  if(result==0):
    escKey()
    return 0, "잉크 클릭 실패"

  randClick(1045,705,10,10,0) #구매
    
  escKey()  #나가기

  return 1, "message:None"


def move_window(sio, data, btn_name, character_name, handle):
  coord=data
  cnt=data[4]
  name=character_name
  win32gui.SetWindowPos(
    handle,
    None,
    320, 180,      # x, y
    0, 0,      # width, height (무시)
    win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
)

  return 1, "message:None"
import serial
import time
import random

ser = serial.Serial('COM3', 9600)

# 랜덤 클릭
def randClick(xVal, yVal, xRange, yRange, clkSleep):
    try:
        if not ser.isOpen():
            ser.open()

        xRange = xVal + xRange
        yRange = yVal + yRange
        if xVal < xRange:
            fromX = xVal
            toX = xRange
        else:
            fromX = xRange
            toX = xVal

        if yVal < yRange:
            fromY = yVal
            toY = yRange
        else:
            fromY = yRange
            toY = yVal

        randX = str(random.randint(fromX, toX))
        randY = str(random.randint(fromY, toY))

        val = f'1!{randX}!{randY}'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break

        time.sleep(clkSleep)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
    return


def randClickRight(xVal, yVal, xRange, yRange, clkSleep):
    try:
        if not ser.isOpen():
            ser.open()

        xRange = xVal + xRange
        yRange = yVal + yRange
        if xVal < xRange:
            fromX = xVal
            toX = xRange
        else:
            fromX = xRange
            toX = xVal

        if yVal < yRange:
            fromY = yVal
            toY = yRange
        else:
            fromY = yRange
            toY = yVal

        randX = str(random.randint(fromX, toX))
        randY = str(random.randint(fromY, toY))

        val = f'11!{randX}!{randY}'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break

        time.sleep(clkSleep)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
    return

# 마우스 드래그
def mouseDrag(dragValues):
    try:
        if not ser.isOpen():
            ser.open()

        randStartX = str(random.randint(dragValues['fromStartX'], dragValues['toStartX']))
        randStartY = str(random.randint(dragValues['fromStartY'], dragValues['toStartY']))
        randEndX = str(random.randint(dragValues['fromEndX'], dragValues['toEndX']))
        randEndY = str(random.randint(dragValues['fromEndY'], dragValues['toEndY']))

        val = f'2!{randStartX}!{randStartY}!{randEndX}!{randEndY}'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
    return

# 키보드 입력
def keyboard(input):
    try:
        if not ser.isOpen():
            ser.open()

        val = f'3!{input}'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
    return

# 첫 마우스 사용 시
def startClick(xVal, yVal, xRange, yRange, clkSleep):
    try:
        if not ser.isOpen():
            ser.open()

        xRange = xVal + xRange
        yRange = yVal + yRange
        if xVal < xRange:
            fromX = xVal
            toX = xRange
        else:
            fromX = xRange
            toX = xVal

        if yVal < yRange:
            fromY = yVal
            toY = yRange
        else:
            fromY = yRange
            toY = yVal
        randX = str(random.randint(fromX, toX))
        randY = str(random.randint(fromY, toY))

        val = f'5!{randX}!{randY}'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
        time.sleep(clkSleep)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
    return

# WIN+b
def winKey():
    try:
        if not ser.isOpen():
            print("오픈!")
            ser.open()

        val = f'7'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
            print("포트 닫힘")
    return

def winKey_1():
    try:
        if not ser.isOpen():
            print("오픈!")
            ser.open()

        val = f'10'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
            print("포트 닫힘")
    return

def escKey():
    try:
        if not ser.isOpen():
            ser.open()

        val = f'9'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
    return

def enterKey():
    try:
        if not ser.isOpen():
            ser.open()

        val = f'6'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
    return

def win_left():
    try:
      if not ser.isOpen():
          ser.open()
      val=f'8'
      val=val.encode('utf-8')
      ser.flushOutput()
      ser.flushInput()
      ser.write(val)
      ser.flush()
      # 완료확인
      while True:
          if ser.in_waiting > 0:
              ret = ser.readline()
              break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.isOpen():
            ser.close()
    return
  

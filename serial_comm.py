import serial
import time
import random
import utils

ser = None

cfg = utils.load_json("client_config.json", "config_json")


# 시리얼 연결
def connect_serial():
    global ser

    try:
        if ser is None or not ser.is_open:
            ser = serial.Serial(
                cfg["serial_port"],
                cfg.get("serial_baudrate", 9600),
                timeout=0.1
            )
            time.sleep(0.5)  # 아두이노 리셋 대기
            print("Serial connected")

        return True

    except Exception as e:
        print("Serial connect failed:", e)
        ser = None
        return False


# 시리얼 연결 종료
def close_serial():
    global ser

    try:
        if ser is not None and ser.is_open:
            ser.close()
            print("시리얼 닫힘")

    except Exception as e:
        print("close_serial error:", e)

    finally:
        ser = None


# 명령 전송 및 ACK 대기
def send_and_wait(cmd, timeout=3.0):
    global ser

    if not connect_serial():
        raise ConnectionError("Serial connection failed")

    try:
        # 입력 버퍼 정리
        ser.reset_input_buffer()

        # 명령 전송
        ser.write((str(cmd) + "\n").encode("utf-8"))
        ser.flush()

        # ACK 대기
        start = time.monotonic()

        while time.monotonic() - start < timeout:
            line = ser.readline().decode(
                errors="ignore"
            ).strip()

            if line == "ACK":
                return True

        raise TimeoutError("Arduino ACK timeout")

    except Exception:
        close_serial()
        raise


# 공통 명령 실행
def execute_command(cmd, delay=0):
    try:
        send_and_wait(cmd)

        if delay > 0:
            time.sleep(delay)

        return True

    except Exception as e:
        print("Error:", e)
        close_serial()
        return False


# 랜덤 좌표 계산
def random_position(value, range_value):
    end = value + range_value
    return random.randint(min(value, end), max(value, end))


# 랜덤 왼쪽 클릭 (명령 1)
def randClick(xVal, yVal, xRange, yRange, clkSleep):
    randX = random_position(xVal, xRange)
    randY = random_position(yVal, yRange)

    val = f'1!{randX}!{randY}'
    return execute_command(val, clkSleep)


# 랜덤 오른쪽 클릭 (명령 11)
def randClickRight(xVal, yVal, xRange, yRange, clkSleep):
    randX = random_position(xVal, xRange)
    randY = random_position(yVal, yRange)

    val = f'11!{randX}!{randY}'
    return execute_command(val, clkSleep)


# 마우스 드래그 (명령 2)
def mouseDrag(dragValues):
    randStartX = random.randint(
        dragValues['fromStartX'],
        dragValues['toStartX']
    )
    randStartY = random.randint(
        dragValues['fromStartY'],
        dragValues['toStartY']
    )
    randEndX = random.randint(
        dragValues['fromEndX'],
        dragValues['toEndX']
    )
    randEndY = random.randint(
        dragValues['fromEndY'],
        dragValues['toEndY']
    )

    val = f'2!{randStartX}!{randStartY}!{randEndX}!{randEndY}'
    return execute_command(val)


# 키보드 입력 (명령 3)
def keyboard(input):
    val = f'3!{input}'
    return execute_command(val)


# 첫 마우스 사용 시 (명령 5)
def startClick(xVal, yVal, xRange, yRange, clkSleep):
    randX = random_position(xVal, xRange)
    randY = random_position(yVal, yRange)

    val = f'5!{randX}!{randY}'
    return execute_command(val)

# ENTER (명령 6)
def enterKey():
    return execute_command('6')

# WIN + B (명령 7)
def winKey():
    return execute_command('7')

# WIN + LEFT (명령 8)
def win_left():
    return execute_command('8')

# ESC (명령 9)
def escKey():
    return execute_command('9')

# 기존 명령 10
def winKey_1():
    return execute_command('10')

def spaceKey():
    return execute_command('12')
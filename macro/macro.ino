//usb cdc 시리얼 통신
#include <Mouse.h>
#include <MouseTo.h>
#include <Keyboard.h>
#include <string.h>
#include <stdlib.h>

// 최대 5개 인자, 각 인자 최대 20글자
char input_data[5][21];
int idx = 0;

// 클릭 및 키보드 딜레이
#define CLICK_HOLD_MS 25
#define KEY_HOLD_MS   30
#define KEY_GAP_MS    10

void setup() {
    Serial.begin(9600);

    Mouse.begin();
    MouseTo.setMaxJump(5);
    MouseTo.setCorrectionFactor(1.215);
    Keyboard.begin();
}

void loop() {
    if (recvData()) {
        handleCommand();
    }
}

// -------------------- 수신 및 파싱 --------------------
bool recvData() {
    static char buffer[128];
    static size_t buf_len = 0;
    static bool overflow = false;

    while (Serial.available() > 0) {
        char c = Serial.read();

        // 명령 종료
        if (c == '\n' || c == '\r') {
            if (overflow) {
                overflow = false;
                buf_len = 0;
                continue;
            }

            if (buf_len == 0) continue;

            buffer[buf_len] = '\0';
            buf_len = 0;

            memset(input_data, 0, sizeof(input_data));
            idx = 0;

            char* token = strtok(buffer, "!");

            while (token != NULL && idx < 5) {
                strncpy(input_data[idx], token, 20);
                input_data[idx][20] = '\0';

                idx++;
                token = strtok(NULL, "!");
            }

            return idx > 0;
        }

        // 데이터 누적
        if (!overflow) {
            if (buf_len < sizeof(buffer) - 1) {
                buffer[buf_len++] = c;
            } else {
                overflow = true;
                buf_len = 0;
            }
        }
    }

    return false;
}

// -------------------- ACK 전송 --------------------
void sendAck() {
    Serial.println("ACK");
}

// -------------------- 키보드 문자열 입력 --------------------
void typeString(const char* str) {
    for (int i = 0; str[i] != '\0'; i++) {
        char c = str[i];

        Keyboard.press(c);
        delay(KEY_HOLD_MS);

        Keyboard.release(c);
        delay(KEY_GAP_MS);
    }
}

// -------------------- 명령 처리 --------------------
void handleCommand() {

    // 1: 랜덤 클릭
    if (strcmp(input_data[0], "1") == 0) {
        int x = atoi(input_data[1]);
        int y = atoi(input_data[2]);

        MouseTo.setTarget(x, y, false);
        while (!MouseTo.move()) {}

        Mouse.press(MOUSE_LEFT);
        delay(CLICK_HOLD_MS);
        Mouse.release(MOUSE_LEFT);
    }

    // 2: 마우스 드래그
    else if (strcmp(input_data[0], "2") == 0) {
        int sx = atoi(input_data[1]);
        int sy = atoi(input_data[2]);
        int ex = atoi(input_data[3]);
        int ey = atoi(input_data[4]);

        MouseTo.setTarget(sx, sy);
        while (!MouseTo.move()) {}

        Mouse.press(MOUSE_LEFT);
        delay(50);

        MouseTo.setTarget(ex, ey, false);
        while (!MouseTo.move()) {}

        delay(50);
        Mouse.release(MOUSE_LEFT);
    }

    // 3: 키보드 문자열 입력 (최대 20글자)
    else if (strcmp(input_data[0], "3") == 0) {
        typeString(input_data[1]);
    }

    // 4: Win + 위쪽 방향키
    else if (strcmp(input_data[0], "4") == 0) {
        Keyboard.press(KEY_LEFT_GUI);
        Keyboard.press(KEY_UP_ARROW);

        delay(KEY_HOLD_MS);
        Keyboard.releaseAll();
    }

    // 5: 첫 마우스 클릭
    else if (strcmp(input_data[0], "5") == 0) {
        int x = atoi(input_data[1]);
        int y = atoi(input_data[2]);

        MouseTo.setTarget(x, y);
        while (!MouseTo.move()) {}

        Mouse.press(MOUSE_LEFT);
        delay(CLICK_HOLD_MS);
        Mouse.release(MOUSE_LEFT);
    }

    // 6: Enter
    else if (strcmp(input_data[0], "6") == 0) {
        Keyboard.press(KEY_RETURN);
        delay(KEY_HOLD_MS);
        Keyboard.release(KEY_RETURN);
    }

    // 7: Win + B
    else if (strcmp(input_data[0], "7") == 0) {
        Keyboard.press(KEY_LEFT_GUI);
        Keyboard.press('b');

        delay(KEY_HOLD_MS);
        Keyboard.releaseAll();
    }

    // 8: Win + 왼쪽 방향키
    else if (strcmp(input_data[0], "8") == 0) {
        Keyboard.press(KEY_LEFT_GUI);
        Keyboard.press(KEY_LEFT_ARROW);

        delay(KEY_HOLD_MS);
        Keyboard.releaseAll();
    }

    // 9: ESC
    else if (strcmp(input_data[0], "9") == 0) {
        Keyboard.press(KEY_ESC);
        delay(KEY_HOLD_MS);
        Keyboard.release(KEY_ESC);
    }

    // 10: Win + 1
    else if (strcmp(input_data[0], "10") == 0) {
        Keyboard.press(KEY_LEFT_GUI);
        Keyboard.press('1');

        delay(KEY_HOLD_MS);
        Keyboard.releaseAll();
    }

    // 11: 마우스 우클릭
    else if (strcmp(input_data[0], "11") == 0) {
        int x = atoi(input_data[1]);
        int y = atoi(input_data[2]);

        MouseTo.setTarget(x, y, false);
        while (!MouseTo.move()) {}

        Mouse.press(MOUSE_RIGHT);
        delay(CLICK_HOLD_MS);
        Mouse.release(MOUSE_RIGHT);
    }

    // 12: Spacebar
    else if (strcmp(input_data[0], "12") == 0) {
        Keyboard.press(' ');
    
        delay(KEY_HOLD_MS);
        Keyboard.release(' ');
    }

    // 명령 처리 완료
    sendAck();

    memset(input_data, 0, sizeof(input_data));
    idx = 0;
}


// // hid 클래스 통신
// #if ARDUINO > 10605
// #include <Mouse.h>
// #endif

// #include <MouseTo.h>
// #include <Keyboard.h>
// #include <HID.h>
// #include <string.h>
// #include <stdlib.h>

// static const uint8_t commandReportDescriptor[] PROGMEM = {
//     0x06, 0x00, 0xFF,  // Usage Page (Vendor Defined)
//     0x09, 0x01,        // Usage
//     0xA1, 0x01,        // Collection (Application)

//     // PC -> Arduino : Output Report ID 3, 63 bytes
//     0x85, 0x03,        // Report ID 3
//     0x09, 0x02,        // Usage
//     0x15, 0x00,        // Logical Minimum 0
//     0x26, 0xFF, 0x00,  // Logical Maximum 255
//     0x75, 0x08,        // Report Size 8
//     0x95, 0x3F,        // Report Count 63
//     0x91, 0x02,        // Output

//     // Arduino -> PC : Input Report ID 4, 3 bytes
//     0x85, 0x04,        // Report ID 4
//     0x09, 0x03,        // Usage
//     0x95, 0x03,        // Report Count 3
//     0x81, 0x02,        // Input

//     0xC0               // End Collection
// };

// // HID 디스크립터 등록
// class CommandDescriptorRegistration {
// private:
//     HIDSubDescriptor node;

// public:
//     CommandDescriptorRegistration()
//         : node(commandReportDescriptor, sizeof(commandReportDescriptor))
//     {
//         HID().AppendDescriptor(&node, HID_IFACE_VENDOR);
//     }
// };

// static CommandDescriptorRegistration commandDescriptorRegistration;


// char input_data[5][10];
// int idx = 0;

// void setup() {
//     Mouse.begin();

//     MouseTo.setMaxJump(5);
//     MouseTo.setCorrectionFactor(1.215);

//     Keyboard.begin();
// }

// void loop() {
//     if (recvData()) {
//         handleCommand();
//     }
// }

// // -------------------- HID 수신 파싱 --------------------
// bool recvData() {

//     uint8_t report[HID_COMMAND_REPORT_SIZE];

//     if (!HID().ReadOutputReport(
//             HID_COMMAND_REPORT_ID,
//             report,
//             sizeof(report))) {
//         return false;
//     }

//     char buffer[HID_COMMAND_REPORT_SIZE + 1];

//     int len = 0;

//     // NULL 또는 줄바꿈까지 명령 추출
//     while (len < HID_COMMAND_REPORT_SIZE &&
//            report[len] != '\0' &&
//            report[len] != '\n') {

//         buffer[len] = (char)report[len];
//         len++;
//     }

//     buffer[len] = '\0';

//     if (len == 0) return false;

//     // 이전 데이터 초기화
//     memset(input_data, 0, sizeof(input_data));

//     idx = 0;

//     char* token = strtok(buffer, "!");

//     while (token != NULL && idx < 5) {

//         strncpy(input_data[idx], token, 9);
//         input_data[idx][9] = '\0';

//         idx++;

//         token = strtok(NULL, "!");
//     }

//     return idx > 0;
// }


// // -------------------- ACK 전송 --------------------
// void sendAck() {

//     const uint8_t ack[HID_ACK_REPORT_SIZE] = {
//         'A', 'C', 'K'
//     };

//     HID().SendReport(
//         HID_IFACE_VENDOR,
//         HID_ACK_REPORT_ID,
//         ack,
//         sizeof(ack)
//     );
// }


// // -------------------- 명령 처리 --------------------
// void handleCommand() {

//     // 1: 랜덤 클릭
//     if (strcmp(input_data[0], "1") == 0) {

//         int x = atoi(input_data[1]);
//         int y = atoi(input_data[2]);

//         MouseTo.setTarget(x, y, false);

//         while (!MouseTo.move()) {}

//         Mouse.click();
//     }

//     // 2: 드래그
//     else if (strcmp(input_data[0], "2") == 0) {

//         int sx = atoi(input_data[1]);
//         int sy = atoi(input_data[2]);
//         int ex = atoi(input_data[3]);
//         int ey = atoi(input_data[4]);

//         MouseTo.setTarget(sx, sy);

//         while (!MouseTo.move()) {}

//         Mouse.press(MOUSE_LEFT);
//         delay(50);

//         MouseTo.setTarget(ex, ey, false);

//         while (!MouseTo.move()) {}

//         delay(50);
//         Mouse.release(MOUSE_LEFT);
//     }

//     // 3: 키보드 입력
//     else if (strcmp(input_data[0], "3") == 0) {

//         Keyboard.print(input_data[1]);
//     }

//     // 4: 윈도우 최대화
//     else if (strcmp(input_data[0], "4") == 0) {

//         Keyboard.press(KEY_LEFT_GUI);
//         Keyboard.press(KEY_UP_ARROW);
//         Keyboard.releaseAll();
//     }

//     // 5: start click
//     else if (strcmp(input_data[0], "5") == 0) {

//         int x = atoi(input_data[1]);
//         int y = atoi(input_data[2]);

//         MouseTo.setTarget(x, y);

//         while (!MouseTo.move()) {}

//         Mouse.click();
//     }

//     // 6: Enter
//     else if (strcmp(input_data[0], "6") == 0) {

//         Keyboard.press(KEY_RETURN);
//         Keyboard.releaseAll();
//     }

//     // 7: Win + B
//     else if (strcmp(input_data[0], "7") == 0) {

//         Keyboard.press(KEY_LEFT_GUI);
//         Keyboard.press('b');
//         Keyboard.releaseAll();
//     }

//     // 8: Win + 왼쪽 방향키
//     else if (strcmp(input_data[0], "8") == 0) {

//         Keyboard.press(KEY_LEFT_GUI);
//         Keyboard.press(KEY_LEFT_ARROW);
//         Keyboard.releaseAll();
//     }

//     // 9: ESC
//     else if (strcmp(input_data[0], "9") == 0) {

//         Keyboard.write(KEY_ESC);
//     }

//     // 10: Win + 1
//     else if (strcmp(input_data[0], "10") == 0) {

//         Keyboard.press(KEY_LEFT_GUI);
//         Keyboard.press('1');
//         Keyboard.releaseAll();
//     }

//     // 11: 우클릭
//     else if (strcmp(input_data[0], "11") == 0) {

//         int x = atoi(input_data[1]);
//         int y = atoi(input_data[2]);

//         MouseTo.setTarget(x, y, false);

//         while (!MouseTo.move()) {}

//         Mouse.click(MOUSE_RIGHT);
//     }

//     // ---- 완료 ACK ----
//     sendAck();

//     // 상태 초기화
//     memset(input_data, 0, sizeof(input_data));
//     idx = 0;
// }


// 파이썬 제어 명령 수신용 FT232RL UART
// #include <HID.h>      

// #if ARDUINO > 10605
// #include <Mouse.h>
// #endif

// #include <MouseTo.h>
// #include <Keyboard.h>
// #include <string.h>
// #include <stdlib.h>

// char input_data[5][10];
// int idx = 0;

// void setup() {
//     // 네이티브 USB는 순수 HID(마우스/키보드) 전용으로 작동
//     Mouse.begin();
//     MouseTo.setMaxJump(5);
//     MouseTo.setCorrectionFactor(1.215);
//     Keyboard.begin();

//     // 파이썬 제어 명령 수신용 FT232RL UART (Serial1) 초기화
//     Serial1.begin(9600);
// }

// void loop() {
//     if (recvData()) {
//         handleCommand();
//     }
// }

// // -------------------- Serial1 (FT232RL) 수신 및 파싱 --------------------
// bool recvData() {
//     static char buffer[128];
//     static int buf_len = 0;

//     while (Serial1.available() > 0) {
//         char c = Serial1.read();
        
//         // 개행 문자(\n 또는 \r)를 만날 때까지 버퍼에 누적
//         if (c == '\n' || c == '\r') {
//             if (buf_len == 0) continue; // 빈 줄 무시
//             buffer[buf_len] = '\0';
//             buf_len = 0; // 다음 수신을 위해 초기화

//             // 이전 데이터 초기화
//             memset(input_data, 0, sizeof(input_data));
//             idx = 0;

//             // '!' 구분자로 토큰 파싱 (기존 로직 유지)
//             char* token = strtok(buffer, "!");

//             while (token != NULL && idx < 5) {
//                 strncpy(input_data[idx], token, 9);
//                 input_data[idx][9] = '\0';
//                 idx++;
//                 token = strtok(NULL, "!");
//             }

//             return idx > 0;
//         } else {
//             if (buf_len < sizeof(buffer) - 1) {
//                 buffer[buf_len++] = c;
//             }
//         }
//     }
//     return false;
// }


// // -------------------- ACK 전송 --------------------
// void sendAck() {
//     // 파이썬 스크립트가 대기하는 "ACK" 응답을 Serial1로 전송
//     Serial1.print("ACK");
// }


// // -------------------- 명령 처리 (기존 로직 유지) --------------------
// void handleCommand() {

//     // 1: 랜덤 클릭
//     if (strcmp(input_data[0], "1") == 0) {

//         int x = atoi(input_data[1]);
//         int y = atoi(input_data[2]);

//         MouseTo.setTarget(x, y, false);

//         while (!MouseTo.move()) {}

//         Mouse.click();
//     }

//     // 2: 드래그
//     else if (strcmp(input_data[0], "2") == 0) {

//         int sx = atoi(input_data[1]);
//         int sy = atoi(input_data[2]);
//         int ex = atoi(input_data[3]);
//         int ey = atoi(input_data[4]);

//         MouseTo.setTarget(sx, sy);

//         while (!MouseTo.move()) {}

//         Mouse.press(MOUSE_LEFT);
//         delay(50);

//         MouseTo.setTarget(ex, ey, false);

//         while (!MouseTo.move()) {}

//         delay(50);
//         Mouse.release(MOUSE_LEFT);
//     }

//     // 3: 키보드 입력
//     else if (strcmp(input_data[0], "3") == 0) {

//         Keyboard.print(input_data[1]);
//     }

//     // // 4: 윈도우 최대화
//     else if (strcmp(input_data[0], "4") == 0) {

//         Keyboard.press(KEY_LEFT_GUI);
//         Keyboard.press(KEY_UP_ARROW);
//         Keyboard.releaseAll();
//     }

//     // 5: start click
//     else if (strcmp(input_data[0], "5") == 0) {

//         int x = atoi(input_data[1]);
//         int y = atoi(input_data[2]);

//         MouseTo.setTarget(x, y);

//         while (!MouseTo.move()) {}

//         Mouse.click();
//     }

//     // 6: Enter
//     else if (strcmp(input_data[0], "6") == 0) {

//         Keyboard.press(KEY_RETURN);
//         Keyboard.releaseAll();
//     }

//     // // 7: Win + B
//     else if (strcmp(input_data[0], "7") == 0) {

//         Keyboard.press(KEY_LEFT_GUI);
//         Keyboard.press('b');
//         Keyboard.releaseAll();
//     }

//     // // 8: Win + 왼쪽 방향키
//     else if (strcmp(input_data[0], "8") == 0) {

//         Keyboard.press(KEY_LEFT_GUI);
//         Keyboard.press(KEY_LEFT_ARROW);
//         Keyboard.releaseAll();
//     }

//     // // 9: ESC
//     else if (strcmp(input_data[0], "9") == 0) {

//         Keyboard.write(KEY_ESC);
//     }

//     // // 10: Win + 1
//     else if (strcmp(input_data[0], "10") == 0) {

//         Keyboard.press(KEY_LEFT_GUI);
//         Keyboard.press('1');
//         Keyboard.releaseAll();
//     }

//     // 11: 우클릭
//     else if (strcmp(input_data[0], "11") == 0) {

//         int x = atoi(input_data[1]);
//         int y = atoi(input_data[2]);

//         MouseTo.setTarget(x, y, false);

//         while (!MouseTo.move()) {}

//         Mouse.click(MOUSE_RIGHT);
//     }

//     // ---- 완료 ACK 전송 ----
//     sendAck();

//     // 상태 초기화
//     memset(input_data, 0, sizeof(input_data));
//     idx = 0;
// }



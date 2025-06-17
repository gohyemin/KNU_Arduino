from arduino_control import Arduino
import time


board = Arduino("9600", port="COM3")

led_pin = 13
board.pinMode(13, "OUTPUT")
board.digitalWrite(13, "LOW")

try:
    while True:
        
        cmd = input("LED ON: 1, OFF: 0, 종료: x → ")

        if cmd == "1":
            board.digitalWrite(led_pin, "HIGH")
            print("💡 LED ON")
        elif cmd == "0":
            board.digitalWrite(led_pin, "LOW")
            print("💡 LED OFF")
        elif cmd.lower() == "x":
            print("종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")

except KeyboardInterrupt:
    print("\n프로그램 강제 종료")
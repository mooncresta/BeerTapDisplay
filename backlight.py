import time
import board
import pwmio

led = pwmio.PWMOut(board.D18, frequency=5000, duty_cycle=0)

while True:
    for i in range(101):
        led.duty_cycle = int(i * 65535 / 100)  # Up
        time.sleep(0.01)
    time.sleep(1)
    for i in range(100, -1, -1):
        led.duty_cycle = int(i * 65535 / 100)  # Down
        time.sleep(0.01)
    time.sleep(1)

import RPi.GPIO as GPIO
import time

# إعداد المنافذ
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
SERVO_PIN = 17

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, 50)

def move_servo(duty):
    servo.start(duty)
    time.sleep(0.5)
    servo.stop()

def read_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    duration = stop_time - start_time
    distance = (duration * 34300) / 2
    return distance

try:
    last_state = None
    while True:
        dist = read_distance()
        print(f"Distance: {dist:.1f} cm")

        if dist <= 20 and last_state != "near":
            move_servo(6.0)  # زاوية 40 درجة تقريبًا
            last_state = "near"

        elif dist > 20 and last_state != "far":
            move_servo(7.5)  # زاوية المنتصف
            last_state = "far"

        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()

# Cotrolling-Servo-Motor-in-Raspberry-pi-5
Cotrolling Servo Motor with Using Ultrasonic

Raspberry pi 5 is used for controlling the servo motor to move 60° if the distance equal or less than 20 cm.

##Here is a brief explanation of the code.

Imports:
import RPi.GPIO as GPIO import time

Import libraries to control GPIO and manage delays.
GPIO Setup:
GPIO.setmode(GPIO.BCM)

Use BCM pin numbering (e.g., GPIO17).
Pin Definitions:
TRIG = 23 ECHO = 24 SERVO_PIN = 17

Define pins for ultrasonic sensor and servo motor.
Pin Modes:
GPIO.setup(TRIG, GPIO.OUT) GPIO.setup(ECHO, GPIO.IN) GPIO.setup(SERVO_PIN, GPIO.OUT)

Set TRIG and SERVO as outputs, ECHO as input.
PWM for Servo:
servo = GPIO.PWM(SERVO_PIN, 50)

Initialize PWM at 50Hz for servo motor.
🔁 Move Servo Function:
def move_servo(duty): servo.start(duty) time.sleep(0.5) servo.stop()

Starts PWM, waits for movement, then stops to reduce jitter.
📏 Distance Measurement Function:
def read_distance(): GPIO.output(TRIG, True) time.sleep(0.00001) GPIO.output(TRIG, False)

Send a 10µs pulse to trigger the ultrasonic sensor. while GPIO.input(ECHO) == 0: start_time = time.time() while GPIO.input(ECHO) == 1: stop_time = time.time()
Record time before and after the echo is received. duration = stop_time - start_time distance = (duration * 34300) / 2 return distance
Calculate distance in cm using speed of sound.
Main Loop:
try: last_state = None while True: dist = read_distance() print(f"Distance: {dist:.1f} cm")

Continuously measure distance and print it. if dist <= 20 and last_state != "near": move_servo(6.0) last_state = "near" elif dist > 20 and last_state != "far": move_servo(7.5) last_state = "far"
Move servo to ~40° if object is near, otherwise return to center. time.sleep(0.2)
Small delay for stability.
❌ Handle Exit:
except KeyboardInterrupt: GPIO.cleanup()

Clean up GPIO when program is interrupted.

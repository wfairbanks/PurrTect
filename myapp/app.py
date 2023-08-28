import cv2
from flask import Flask, render_template, Response, request
import RPi.GPIO as GPIO
from time import sleep

app = Flask(__name__)

# Servo pin configurations
SERVO_PAN_PIN = 17
SERVO_TRIGGER_PIN = 27

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PAN_PIN, GPIO.OUT)
GPIO.setup(SERVO_TRIGGER_PIN, GPIO.OUT)

pan_servo = GPIO.PWM(SERVO_PAN_PIN, 50)
trigger_servo = GPIO.PWM(SERVO_TRIGGER_PIN, 50)

pan_servo.start(0)
trigger_servo.start(0)

# Load the pre-trained model for cat detection
cat_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalcatface.xml")

def detect_cat(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cats = cat_cascade.detectMultiScale(gray, 1.1, 5)
    for (x, y, w, h) in cats:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return frame, cats

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame, cats = detect_cat(frame)
        if cats:
            # Code to move the servo to align with the cat
            pan_servo.ChangeDutyCycle(7.5)  # Assuming 7.5 as the middle position
            sleep(1)
            trigger_servo.ChangeDutyCycle(2.5)  # Pull the trigger
            sleep(1)
            trigger_servo.ChangeDutyCycle(7.5)  # Reset trigger position
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move/<direction>', methods=['GET'])
def move(direction):
    if direction == "trigger":
        # Code to activate the spray
        trigger_servo.ChangeDutyCycle(2.5)
        sleep(1)
        trigger_servo.ChangeDutyCycle(7.5)
    else:
        # Optionally: Move the pan servo based on other commands
        pass
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

import cv2
import os
from flask import Flask, render_template, Response, request
from time import sleep

# Initialize Flask app
app = Flask(__name__)

# Check if running on Raspberry Pi
GPIO.setwarnings(False)
ON_RASPBERRY_PI = False
try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    ON_RASPBERRY_PI = True
except (ImportError, RuntimeError):
    print("RPi.GPIO not available. Mocking GPIO functionalities.")

# Servo pin configurations
SERVO_PAN_PIN = 17
SERVO_TRIGGER_PIN = 27

if ON_RASPBERRY_PI:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PAN_PIN, GPIO.OUT)
    GPIO.setup(SERVO_TRIGGER_PIN, GPIO.OUT)
    pan_servo = GPIO.PWM(SERVO_PAN_PIN, 50)
    trigger_servo = GPIO.PWM(SERVO_TRIGGER_PIN, 50)
    pan_servo.start(0)
    trigger_servo.start(0)
else:
    # Define mock methods here, if needed
    class MockGPIO:
        BCM = None
        OUT = None

        @staticmethod
        def setmode(mode):
            pass

        @staticmethod
        def setup(pin, mode):
            pass

        @staticmethod
        def PWM(pin, freq):
            class MockPWM:
                def start(self, value):
                    pass

                def ChangeDutyCycle(self, value):
                    pass

            return MockPWM()

    GPIO = MockGPIO
    pan_servo = GPIO.PWM(SERVO_PAN_PIN, 50)
    trigger_servo = GPIO.PWM(SERVO_TRIGGER_PIN, 50)
    pan_servo.start(0)
    trigger_servo.start(0)

# Load the pre-trained model for cat detection


xml_path = "/home/wfairbanks/Projects/purrtect/myapp/haarcascade_frontalcatface.xml"

# Load the cascade classifier
if os.path.exists(xml_path):
    cat_cascade = cv2.CascadeClassifier(xml_path)
else:
    print("XML file not found.")

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

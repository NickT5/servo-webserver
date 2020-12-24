import json
from time import sleep
import RPi.GPIO as GPIO
from flask import Flask, request

app = Flask(__name__)


def angle_to_duty_cycle(angle: float) -> float:
    """
    convert angle to duty cycle
    """
    try:
        dc = (1.0/18.0 * angle) + 2
    except TypeError:
        dc = None
    return dc


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/servo")
def set_servo_angle():
    # e.g. http://<rpi-ip>:<port>/servo?angle=90
    angle = request.args.get('angle', type=float)
    duty_cycle = angle_to_duty_cycle(angle)

    if duty_cycle is None:
        response: dict = {
	    "angle": angle,
	    "duty_cycle": duty_cycle,
	    "status": 400
        }
    else:
        GPIO.output(SERVO_PIN, True)
        pwm.ChangeDutyCycle(duty_cycle)

        sleep(1)  # give time for servo to turn

        # turn off pwm to stop buzzing
        # buzzing might go away if we
        # use a diff power source for the motor
        GPIO.output(SERVO_PIN, False)
        pwm.ChangeDutyCycle(0)

        response: dict = {
	    "angle": angle,
	    "duty_cycle": duty_cycle,
	    "status": 200
        }

    return json.dumps(response)


if __name__ == "__main__":
    # setup gpio pin for servo
    GPIO.setmode(GPIO.BOARD)
    SERVO_PIN = 3
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    # setup pwm for servo
    FREQUENCY = 50
    pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
    pwm.start(0)
    # setup server
    PORT = 5001
    print(f"Server is listening on port {PORT}")
    app.run(debug=True, host="0.0.0.0", port=PORT)

    # tear down
    pwm.stop()
    GPIO.cleanup()

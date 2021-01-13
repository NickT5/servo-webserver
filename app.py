#! /usr/bin/python3

import json
from time import sleep
import RPi.GPIO as GPIO
from flask import Flask, request

app = Flask(__name__)


def angle_to_duty_cycle(angle: float) -> float:
    """
    convert angle to duty cycle
    Works with servo motor Tower Pro SG92R.
    Works not with servo motor Tower Pro SG90
    """
    try:
        dc = (1.0/18.0 * angle) + 2
    except TypeError:
        dc = None
    return dc


def set_angle(angle: float) -> dict:
    """
    Change the angle of the servo motor
    :param angle: the angle to rotate to
    :return: response dictionary
    :rtype: dict
    """
    duty_cycle = angle_to_duty_cycle(angle)
    r: dict = set_duty_cycle(duty_cycle)
    return r


def set_duty_cycle(duty_cycle: float) -> dict:
    """
    Change the pwm duty cycle of the servo motor
    :param duty_cycle: the duty cycle to be set on the servo pin
    :return: response dictionary
    :rtype: dict
    """
    if duty_cycle is None:
        response: dict = {
            "duty_cycle": duty_cycle,
            "status": 400,
            "reason": "duty cycle is None"
        }
    else:
        pwm.ChangeDutyCycle(duty_cycle)

        response: dict = {
            "duty_cycle": duty_cycle,
            "status": 200
        }
    return response


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/servo")
def set_servo_angle():
    angle = request.args.get("angle", type=float)
    duty_cycle = request.args.get("duty_cycle", type=float)

    if angle is not None:
        response: dict = set_angle(angle)
    elif duty_cycle is not None:
        response: dict = set_duty_cycle(duty_cycle)
    else:
        response = {
            "status": 400,
            "reason": "not satisfied with url parameter"
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

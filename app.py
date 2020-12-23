import RPi.GPIO as GPIO
from flask import Flask, request
app = Flask(__name__)


def angle_to_duty_cycle(angle: float) -> float:
    """
    convert angle to duty cycle
    :param angle:
    :return:
    """
    return (1.0/18.0 * angle) + 2


@app.route('/')
def hello_world():
    return 'Hello, World!'


# http://localhost:5000/servo?angle=5
@app.route("/servo")
def set_angle():
    angle = request.args.get('angle')
    try:
        angle = float(angle)
    except:
        pass

    return angle


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    SERVO_PIN = 3
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    FREQUENCY = 50
    pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
    pwm.start(0)

    app.run(debug=True)

    print("hello")

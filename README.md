# Servo control via webserver
Control a servo motor via a webserver running on a Raspberry Pi.

## Run webserver
`python3 app.py`

## API
### Call
* http://\<rpi-ip-addr\>:\<port\>__/servo?angle=\<angle\>__
* http://\<rpi-ip-addr\>:\<port\>__/servo?duty_cycle=\<dc\>__
### Response
Responses are in json. There's a status field to check if the api request was successful.
Note:
With the servo motor i'm using, these duty cycles corresponds to zero and 180°:
* duty cycle of 2 ~ 0°
* duty cycle of 12 ~ 180°

## Hardware
* Raspberry Pi 2 model B v1.1
* Servo motor Tower Pro SG92R
  - GND (brown) to GND
  - VCC (red) to 5V
  - PWM (yellow) to GPIO pin 3

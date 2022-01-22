from flask import Flask, request
import raw_led_handler
import time

app = Flask(__name__)

lights = raw_led_handler.raw_leds()


@app.route('/update')
def update():
    lights.update()
    return "updated"

@app.route('/pixel/<int:n>/<s>')
def pixel(n, s):
    lights.set_pixel(n, s)
    return "set"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=False)

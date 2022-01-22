from flask import Flask, request
import leds
import time

app = Flask(__name__)

lights = leds.light_strip(is_receiver=True)


@app.route('/update')
def update():
    lights.update()
    return "updated"

@app.route('/pixel/<int:n>/<int:g>/<int:b>/<int:r>')
def pixel(n, g, b, r):
    lights.set_pixel(n, (g, b, r))
    return "set"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=False)

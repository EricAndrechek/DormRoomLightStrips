from flask import Flask, request
import leds
import time

app = Flask(__name__)

lights = leds.light_strip()


@app.route('/status')
def status():
    region = request.args.get('r')
    return str(lights.status(region))

@app.route('/on')
def on():
    region = request.args.get('r')
    lights.region_on(region)
    return 'on'

@app.route('/off')
def off():
    region = request.args.get('r')
    lights.region_off(region)
    return 'off'

@app.route('/color')
def color():
    region = request.args.get('r')
    return lights.get_hex(region)

@app.route('/cset/<s>')
def cset(s):
    region = request.args.get('r')
    lights.region_color(region, s)
    return 'set'

@app.route('/bset/<s>')
def bset(s):
    region = request.args.get('r')
    lights.set_brightness(region, s)
    return 'set'

@app.route('/bright')
def brightness():
    region = request.args.get('r')
    return lights.get_brightness(region)

if __name__ == '__main__':
    lights.all_off()
    app.run(host="0.0.0.0", port=8000, debug=True)
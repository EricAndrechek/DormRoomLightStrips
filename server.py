from flask import Flask, request
import leds
import time

app = Flask(__name__)

lights = leds.light_strip(is_receiver=True)


@app.route('/status')
def status():
    region = request.args.get('r')
    return str(lights.status(region))


@app.route('/on')
def on():
    region = request.args.get('r')
    lights.region_on(region)
    lights.update()
    return 'on'


@app.route('/off')
def off():
    region = request.args.get('r')
    lights.region_off(region)
    lights.update()
    return 'off'


@app.route('/color')
def color():
    region = request.args.get('r')
    return lights.get_hex(region)


@app.route('/cset/<s>')
def cset(s):
    region = request.args.get('r')
    lights.region_color(region, s)
    lights.update()
    return 'set'


@app.route('/bset/<s>')
def bset(s):
    region = request.args.get('r')
    lights.set_brightness(region, s)
    lights.update()
    return 'set'


@app.route('/bright')
def brightness():
    region = request.args.get('r')
    return str(lights.get_brightness(region))


@app.route('/custom/<switch>')
def example(switch):
    todo = request.args.get('r')
    data = request.args.get('s')
    if todo == 'status':
        lights.status(switch)
    elif todo == 'on':
        lights.switch_on(switch, lights)
    elif todo == 'off':
        lights.switch_off(switch)
    elif todo == 'color':
        lights.get_hex(switch)
    elif todo == 'bright':
        lights.switch_brightness(switch)
    elif todo == 'cset':
        lights.switch_on(switch, lights, color=data)
    elif todo == 'bset':
        lights.switch_on(switch, lights, brightness=data)



if __name__ == '__main__':
    lights.all_off()
    app.run(host="0.0.0.0", port=8000, debug=False)

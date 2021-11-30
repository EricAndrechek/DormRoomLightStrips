from flask import Flask
import leds
import time

app = Flask(__name__)

lights = leds.light_strip()

'''
Everything below is for the entire light strip
--------------------------------------------------------------------------------
'''

@app.route('/status')
def status():
    return str(lights.status())

@app.route('/on')
def on():
    lights.on()
    return 'on'

@app.route('/off')
def off():
    lights.off()
    return 'off'

@app.route('/color')
def color():
    return lights.get_hex()

@app.route('/cset/<s>')
def cset(s):
    print("\"" + s + "\"")
    lights.set_hex(s)
    return 'set'

@app.route('/bset/<s>')
def bset(s):
    return 'sorry this does nothing' 
    # jayden figure out if this is possible if you want to help

@app.route('/bright')
def brightness():
    return "100" if lights.status() == 1 else "0"

'''
Everything below is for 
'''

if __name__ == '__main__':
    lights.off()
    app.run(host="0.0.0.0", port=8000, debug=True)
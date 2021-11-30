from flask import Flask
import leds
import time

app = Flask(__name__)

lights = leds.light_strip()

'''
Everything below is for the entire light strip
--------------------------------------------------------------------------------
'''

@app.route('/main/status')
def main_status():
    return str(lights.status())

@app.route('/main/on')
def main_on():
    lights.on()
    return 'on'

@app.route('/main/off')
def main_off():
    lights.off()
    return 'off'

@app.route('/main/color')
def main_color():
    return lights.get_hex()

@app.route('/main/cset/<s>')
def main_cset(s):
    lights.set_hex(s)
    return 'set'

@app.route('/main/bset/<s>')
def main_bset(s):
    return 'sorry this does nothing' 
    # jayden figure out if this is possible if you want to help

@app.route('/main/bright')
def main_brightness():
    return "100" if lights.status() == 1 else "0"

'''
Everything below is for 
'''

if __name__ == '__main__':
    lights.off()
    app.run(host="0.0.0.0", port=8000, debug=True)
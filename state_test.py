import leds

def main(lights):
    # put whatever you want the switch to do here
    # it can call other functions located within this file
    print(lights.status("main"))

if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
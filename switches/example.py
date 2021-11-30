import leds

def main(lights):
    # put whatever you want the switch to do here
    # it can call other functions located within this file
    lights.set_hex("ffffff")

if __name__ == '__main__':
    lights = leds.Leds()
    main(lights)
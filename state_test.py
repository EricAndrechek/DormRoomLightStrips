import leds

def main(lights):
    # put whatever you want the switch to do here
    # it can call other functions located within this file
    print(lights.get_all_states())

if __name__ == '__main__':
    lights = leds.Leds()
    main(lights)
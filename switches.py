import os
import click
import json

from nbformat import write

@click.group()
def cli():
    pass


@cli.command()
@cli.option('--dry-run', help='Run the code without actually executing it', is_flag=True)
def build_server(dry_run):
    pass


@cli.command()
@cli.option('--dry-run', help='Run the code without actually executing it', is_flag=True)
def build_devices(dry_run):
    # open switches.json
    with open('switches.json') as f:
        switches = json.load(f)

    # append the switches to devices.json
    with open("devices.json", "r") as f:
        devices = json.load(f)

    new_devices = {}
    for switch in switches:
        new_switch_device = {"accessory": "HttpPushRgb", "service": "Light", "switch": {}}
        new_switch_device["name"] = switch["name"]
        new_switch_device["switch"]["notificationID"] = switch["internal_name"]
        new_switch_device["switch"]["status"] = "http://192.168.2.97:8000/status?r=" + switch["internal_name"]
        new_switch_device["switch"]["powerOn"] = "http://192.168.2.97:8000/on?r=" + switch["internal_name"]
        new_switch_device["switch"]["powerOff"] = "http://192.168.2.97:8000/off?r=" + switch["internal_name"]

        if switch["is_brightness_slider"]:
            new_switch_device["switch"]["brightness"] = {}
            new_switch_device["switch"]["brightness"]["max"] = switch["brightness_slider_max"]
            new_switch_device["switch"]["brightness"]["status"] = "http://192.168.2.97:8000/bright?r=" + switch["internal_name"]
            new_switch_device["switch"]["brightness"]["url"] = "http://192.168.2.97:8000/bset/%s?r=" + switch["internal_name"]
        
        if switch["is_rgb"]:
            new_switch_device["switch"]["color"] = {}
            new_switch_device["switch"]["color"]["brightness"] = False
            new_switch_device["switch"]["color"]["status"] = "http://192.168.2.97:8000/color?r=" + switch["internal_name"]
            new_switch_device["switch"]["color"]["url"] = "http://192.168.2.97:8000/cset/%s?r=" + switch["internal_name"]
        
        new_devices.append(new_switch_device)
    
    for new_device in new_devices:
        for device in devices:
            if device["name"] == new_device["name"]:
                devices.remove(device)
                break
        devices.append(new_device)

    if not dry_run:
        with open("devices.json", "w") as f:
            json.dump(devices, f)
    else:
        with open("devices-staging.json", "w") as f:
            json.dump(devices, f)
        print("Wrote devices-staging.json")
        


@cli.command()
@cli.option('--dry-run', help='Run the code without actually executing it', is_flag=True)
def compile(dry_run):
    # read all files in switches folder and parse their first 6 lines
    files = os.listdir("switches")
    switches = []
    for file in files:
        if file.endswith(".py"):
            with open("switches/" + file, "r") as f:
                # get the first 5 lines
                lines = f.readlines()[0:5]
                # parse the lines
                name = lines[0].split(":")[1].split('#')[0].strip()
                internal_name = lines[1].split(":")[1].split('#')[0].strip()
                is_brightness_slider = lines[2].split(":")[1].split('#')[0].strip()
                is_brightness_slider = is_brightness_slider == "True"
                brightness_slider_max = int(lines[3].split(":")[1].split('#')[0].strip())
                is_rgb = lines[3].split(":")[1].split('#')[0].strip()
                is_rgb = is_rgb == "True"
                description = lines[4].split(":")[1].split('#')[0].strip()
                switches.append({"name": name, "internal_name": internal_name, "is_brightness_slider": is_brightness_slider, "brightness_slider_max": brightness_slider_max, "is_rgb": is_rgb, "description": description})

    if dry_run:
        # print the switches
        for switch in switches:
            print("Friendly name: " + switch["name"])
            print("Internal name: " + switch["internal_name"])
            print("Brightness slider: " + str(switch["is_brightness_slider"]))
            print("Brightness slider max: " + switch["brightness_slider_max"])
            print("RGB: " + str(switch["is_rgb"]))
            print("Description: " + switch["description"])
            print("")
    else:
        write_buffer = ""
        for switch in switches:
            # add switch name, description, and whether or not it takes brightness or rgb (and if so what the max is) to the switches text file
            write_buffer += "Switch name: " + switch["name"] + "\n"
            write_buffer += "Description: " + switch["description"] + "\n"
            write_buffer += "File name: " + switch["internal_name"] + ".py\n"
            if switch["is_brightness_slider"]:
                write_buffer += "Brightness slider\n"
                write_buffer += "Max brightness: " + str(switch["brightness_slider_max"]) + "\n"
            if switch["is_rgb"]:
                write_buffer += "RGB slider\n"
            write_buffer += "\n"
        with open("switches.txt", "w") as f:
            f.write(write_buffer)
        
        # save the switches to switches.json
        with open("switches.json", "w") as f:
            json.dump(switches, f)


if __name__ == '__main__':
    cli()
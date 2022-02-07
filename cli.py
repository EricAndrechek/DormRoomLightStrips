import os
import click
import json

@click.group()
@click.option('--dry-run', help='Run the code without actually executing it', is_flag=True, default=False)
@click.pass_context
def cli(ctx, dry_run):
    ctx.ensure_object(dict)

    ctx.obj['dry_run'] = dry_run


@cli.command()
@click.option('--search', help='Search for a switch by name or description')
def list(search):
    # if search is not none then look for matching text in the name or description of switches.json file and pretty print the results
    # otherwise just print the switches.txt file
    if search is not None:
        write_buffer = ""
        with open('switches.json') as switches:
            switches = json.load(switches)
            for switch in switches:
                if search.lower() in switch['name'].lower() or search.lower() in switch['description'].lower():
                    write_buffer += "Switch name: " + switch["name"] + "\n"
                    write_buffer += "Description: " + switch["description"] + "\n"
                    write_buffer += "File name: " + switch["internal_name"] + ".py\n"
                    if switch["is_brightness_slider"]:
                        write_buffer += "Brightness slider\n"
                        write_buffer += "Max brightness: " + str(switch["brightness_slider_max"]) + "\n"
                    if switch["is_rgb"]:
                        write_buffer += "RGB slider\n"
                    write_buffer += "\n"
        if write_buffer == "":
            print("No switches found matching the search term")
        else:
            print(write_buffer)
    else:
        with open('switches.txt') as switches:
            print(switches.read())


@cli.command()
@click.pass_context
@click.option('--dry-run', help='Run the code without actually executing it', is_flag=True, default=False)
def build_init(ctx, dry_run):
    dry_run = dry_run or ctx.obj['dry_run']
    # add all internal names to a list and write list to switches/__init__.py
    with open('switches.json') as switches:
        switches = json.load(switches)
        switchlist = []
        for switch in switches:
            switchlist.append(switch['internal_name'])
        write_buffer = "__all__ = [" + ", ".join(f'"{switch}"' for switch in switchlist) + "]"
        if not dry_run:
            with open('switches/__init__.py', 'w') as init:
                init.write(write_buffer)
        else:
            print(write_buffer)


@cli.command()
@click.pass_context
@click.option('--dry-run', help='Run the code without actually executing it', is_flag=True, default=False)
def build_devices(ctx, dry_run):
    dry_run = dry_run or ctx.obj['dry_run']
    # open switches.json
    with open('switches.json') as f:
        switches = json.load(f)

    # append the switches to devices.json
    with open("devices.json", "r") as f:
        devices = json.load(f)

    new_devices = []
    for switch in switches:
        new_switch_device = {"accessory": "HttpPushRgb", "name": switch["name"], "service": "Light", "switch": {}}
        new_switch_device["switch"]["notificationID"] = switch["internal_name"]
        new_switch_device["switch"]["status"] = "http://raspberrypi.local:8000/custom/" + switch["internal_name"] + "?r=status"
        new_switch_device["switch"]["powerOn"] = "http://raspberrypi.local:8000/custom/" + switch["internal_name"] + "?r=on"
        new_switch_device["switch"]["powerOff"] = "http://raspberrypi.local:8000/custom/" + switch["internal_name"] + "?r=off"

        if switch["is_brightness_slider"]:
            new_switch_device["brightness"] = {}
            new_switch_device["brightness"]["max"] = switch["brightness_slider_max"]
            new_switch_device["brightness"]["status"] = "http://raspberrypi.local:8000/custom/" + switch["internal_name"] + "?r=bright"
            new_switch_device["brightness"]["url"] = "http://raspberrypi.local:8000/custom/" + switch["internal_name"] + "?r=bset&s=%s"
        
        if switch["is_rgb"]:
            new_switch_device["color"] = {}
            new_switch_device["color"]["brightness"] = False
            new_switch_device["color"]["status"] = "http://raspberrypi.local:8000/custom/" + switch["internal_name"] + "?r=color"
            new_switch_device["color"]["url"] = "http://raspberrypi.local:8000/custom/" + switch["internal_name"] + "?r=cset&s=%s"
        
        new_devices.append(new_switch_device)
    
    for new_device in new_devices:
        for device in devices:
            if device["name"] == new_device["name"]:
                devices.remove(device)
                break
        devices.append(new_device)

    if not dry_run:
        with open("devices.json", "w") as f:
            json.dump(devices, f, indent=4)
    else:
        with open("devices-staging.json", "w") as f:
            json.dump(devices, f, indent=4)
        print("Wrote devices-staging.json")
        


@cli.command()
@click.pass_context
@click.option('--dry-run', help='Run the code without actually executing it', is_flag=True, default=False)
def compile(ctx, dry_run):
    dry_run = dry_run or ctx.obj['dry_run']
    # read all files in switches folder and parse their first 6 lines
    files = os.listdir("switches")
    switches = []
    for file in files:
        if file.endswith(".py") and not file.startswith("__"):
            with open("switches/" + file, "r") as f:
                # get the first 5 lines
                lines = f.readlines()[0:6]
                # parse the lines
                name = lines[0].split(":")[1].split('#')[0].strip()
                internal_name = lines[1].split(":")[1].split('#')[0].strip()
                is_brightness_slider = lines[2].split(":")[1].split('#')[0].strip()
                is_brightness_slider = is_brightness_slider == "True"
                brightness_slider_max = int(lines[3].split(":")[1].split('#')[0].strip())
                is_rgb = lines[4].split(":")[1].split('#')[0].strip()
                is_rgb = is_rgb == "True"
                description = lines[5].split(":")[1].split('#')[0].strip()
                if name != "Example":
                    switches.append({"name": name, "internal_name": internal_name, "is_brightness_slider": is_brightness_slider, "brightness_slider_max": brightness_slider_max, "is_rgb": is_rgb, "description": description})

    if dry_run:
        # print the switches
        for switch in switches:
            print("Friendly name: " + switch["name"])
            print("Internal name: " + switch["internal_name"])
            print("Brightness slider: " + str(switch["is_brightness_slider"]))
            print("Brightness slider max: " + str(switch["brightness_slider_max"]))
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
            json.dump(switches, f, indent=4)


if __name__ == '__main__':
    cli(obj={})
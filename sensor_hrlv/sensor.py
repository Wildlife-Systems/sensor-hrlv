#!/usr/bin/python3

import sys
import time
import os
import json
import serial

def get_serial_number():
    """Retrieve the Raspberry Pi's serial number."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("Serial"):
                    return line.split(":")[1].strip() + "_hrlv"
    except FileNotFoundError:
        print("Error: Unable to access /proc/cpuinfo. Are you running this on a Raspberry Pi?")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def cli():
    """Command line interface for the HRLV sensor."""
    if len(sys.argv) == 2:
        if sys.argv[1] == "identify":
            identify()
        elif sys.argv[1] == "list":
            list_sensors()
        else:
            read_sensor()
            sys.exit(0)
    else:
        read_sensor()
        sys.exit(0)

def identify():
    """Identify the sensor."""
    sys.exit(60)

def list_sensors():
    """List available sensors."""
    print("distance")
    sys.exit(0)

def read_sensor():
    sensor_json = ""
    """Read JSON from /etc/ws/hrlv.json"""
    if os.path.exists("/etc/ws/hrlv.json"):
        #Create empty array
        with open("/etc/ws/hrlv.json") as f:
            data = json.load(f)
        # Loop over JSON objects in data array
        for sensor in data:
            if "internal" in sensor:
                internal = sensor["internal"]
            else:
                internal = False
            if "sensor_id" in sensor:
                sensor_id = sensor["sensor_id"]
            else:
                sensor_id = get_serial_number()
            json_string = read_sensor_helper(internal, sensor_id)
            #Merge the JSON arrays in strings sensor_json and json_string
            if sensor_json == "":
                sensor_json = json_string
            else:
                sensor_json = sensor_json[:-1] + "," + json_string[1:]
        print(sensor_json)
        return

    else:
        print(read_sensor_helper())
        return

def read_sensor_helper(internal=False, sensor_id=get_serial_number()):

    reads = 0
    total = 0

    while reads <= 20:

        try:
            ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

            data = ser.read_until(b'\r')

            range = int(data[2:-1])

            reads = reads + 1

            total = total + range

        except KeyboardInterrupt:

            exit(0)

        except:

            continue

    value = round(total/reads, 1)/1000

    stream = os.popen('sc-prototype')
    output = stream.read()
    outjs = json.loads(output)

    outjs["sensor"] = "ultrasound_distance"
    outjs["measures"] = "distance"
    outjs["unit"] = "metres"
    outjs["value"] = value
    outjs["sensor_id"] = sensor_id
    outjs["internal"] = internal

    ret = "[" + json.dumps(outjs) + "]"
    return ret

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "identify":
            identify()
        elif sys.argv[1] == "list":
            list_sensors()

    data = read_sensor()
    print(json.dumps(data))

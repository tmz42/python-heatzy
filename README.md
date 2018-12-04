# python-heatzy - Python Heatzy controller
## heatzy
Heatzy (https://heatzy.com/) is a provider of heating control solutions (such as Pilot Wire addons to radiators). There is an API available on Google Drive, this software was created to control the Pilot Wire solution from a Python library.
## Usage
### Python
```python
# First create the handler with your heatzy app login/password
hh = HeatzyHandler('bidon@bidon.fr', 'p@ssw0rd')

# Get the devices (HeatzyDevice) associated to your account
deviceDict = hh.getHeatzyDevices()

for device_name in deviceDict:
    hd = deviceDict[device_name]
    hd.status()         # Returns the status (OFF, ECO, HGEL, CONFORT)
    hd.confort()        # Sets the instruction to confort
    hd.stop()           # Sets to OFF
```
### CLI
A CLI tool for interacting with the library is included (bin/heatzy-cli)
```bash
python .\heatzy.py
usage: heatzy.py [-h] [-u USERNAME] [-p PASSWORD] [-d DEVICE] [-l]
                 [-m SETMODE]

Controls Heatzy devices throught the CLI

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username on the Heatzy (Gizwits) platform
  -p PASSWORD, --password PASSWORD
                        Password of the user
  -d DEVICE, --device DEVICE
                        Name of the Heatzy device you wish to control
  -l, --list            List all devices
  -m SETMODE, --setmode SETMODE
                        Sets the mode of the device
python heatzy.py -u login@heatzy.com -p p@ssw0rd -l                        # Lists the devices
python heatzy.py -u login@heatzy.com -p p@ssw0rd -d Bedroom                # Prints the info of the device
python heatzy.py -u login@heatzy.com -p p@ssw0rd -d Bedroom -m ECO         # Sets the device in the bedroom in ECO mode
```

### MQTT Daemon
A MQTT Daemon is included to interact remotely with a MQTT-enabled home automation software (this was created with Home Assistant in mind)
```bash
python .\heatzy-mqtt
usage: heatzy-mqtt [-h] [-u USERNAME] [-p PASSWORD] [-s SERVER] [-i PORT]

Controls Heatzy devices throught the CLI

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username on the Heatzy (Gizwits) platform
  -p PASSWORD, --password PASSWORD
                        Password of the user
  -s SERVER, --server SERVER
                        Broker IP or hostname
  -i PORT, --port PORT  Broker MQTT Port (default : 1883)
  ```
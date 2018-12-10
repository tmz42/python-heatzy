# python-heatzy - Python Heatzy controller
## heatzy
Heatzy (https://heatzy.com/) is a provider of heating control solutions (such as Pilot Wire addons to radiators). There is an API available on Google Drive, this software was created to control the Pilot Wire solution from a Python library.
## Usage
### Python
```python
>>> import heatzy
# First create the handler with your heatzy app login/password
>>> hh = heatzy.HeatzyHandler('bidon@bidon.fr', 'p@ssw0rd')

# Get the devices dictionary (containing object type HeatzyDevice) associated to your account. The key is the device name
>>> deviceDict = hh.getHeatzyDevices()

# Assigns the device named 'Chambre'
>>> device = deviceDict['Chambre']  
# Gets status
>>> device.status() 
'ECO'
### Sets 'confort' mode 
>>> device.confort()
# Gets status
>>> device.status() 
'CONFORT'
>>> device.off()            # Sets mode to 'off'
>>> device.horsgel()        # Anti-freezing mode
>>> device.eco()            # Sets 'ECO' mode
>>> device.setMode('ECO')   # Different way to set 'ECO' mode

```
### CLI
A CLI tool for interacting with the library is included (bin/heatzy-cli)
```bash
heatzy-cli
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
heatzy-cli -u login@heatzy.com -p p@ssw0rd -l                        # Lists the devices
heatzy-cli -u login@heatzy.com -p p@ssw0rd -d Bedroom                # Prints the info of the device
heatzy-cli -u login@heatzy.com -p p@ssw0rd -d Bedroom -m ECO         # Sets the device in the bedroom in ECO mode
```
### HASS Integration
An optional component is available under opt/homeassistant. Put it in your '<config>/custom_components/climate' directory, and edit your configuration.yaml file.

```YAML
# Heatzy
climate:
  - platform: heatzy
    username: 'bidon@bidon.com'
    password: 'p@ssw0rd'
```
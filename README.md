# Python Heatzy controller
## heatzy
Heatzy (https://heatzy.com/) is a provider of heating control solutions (such as Pilot Wire addons to radiators). There is an API available on Google Drive, this software was created to control the Pilot Wire solution from a Python library.
## Usage
```python
from heatzy import HeatzyHandler, HeatzyDevice

# First create the handler with your heatzy app login/password
hh = HeatzyHandler('bidon@bidon.fr', 'p@ssw0rd')

# Get the devices associated to your account
deviceList = hh.getHeatzyDevices()

for device in deviceList:
    device.status()         # Returns the status (OFF, ECO, HGEL, CONFORT)
    device.confort()        # Sets the instruction to confort 
    device.stop()           # Sets to OFF

```
# python-heatzy - Python Heatzy controller
## heatzy
Je dispose chez moi de devices Heatzy, qui me permettent de gérer simplement le mode de mon chauffage. A partir de l'API disponible sur Google Drive, j'ai écrit ce package python (disponible également sur PyPi).

Elle ne gère (pour l'instant en tout cas) ni la programmation ni les Heatzy Flam. 

## Usage
### Installation
Vous pouvez l'installer depuis PyPi avec pip :
```bash
$ pip install 
```

Vous pouvez également l'installer depuis la source :
```bash
$ git clone https://github.com/tmz42/python-heatzy.git
$ cd python-heatzy
$ python setup.py install
```
### Python
Le package heatzy propose deux classes :
- HeatzyHandler, qui gère la connexion à l'API et génère les devices
- HeatzyDevice, qui correspond à un device heatzy installé et associé à votre compte.

Voici comment l'utiliser :
```python
>>> import heatzy
# Créez en premier lieu le Handler avec votre login/password utilisés dans l'application.
# L'opération de login se fait automatiquement, et génère une exception en cas de crash
>>> hh = heatzy.HeatzyHandler('bidon@bidon.fr', 'p@ssw0rd')

# Cette ligne récupère tous les devices associés à votre compte sous forme de dictionnaire
>>> deviceDict = hh.getHeatzyDevices()

# Jouons avec le device nommé Chambre
>>> device = deviceDict['Chambre']  
# Quel est son état?
>>> device.status() 
'ECO' # Cela aurait pu être 'OFF', 'HGEL', 'ECO' ou 'CONFORT'
# Passons-le en mode confort...
>>> device.confort()
# Et vérifions si cela a marché.
>>> device.status() 
'CONFORT'
>>> device.off()            # On le passe en mode délestage
>>> device.horsgel()        # On le passe en mode hors gel
>>> device.eco()            # On le passe en mode eco
>>> device.setMode('ECO')   # Une autre façon de changer le mode ('OFF', 'HGEL', 'ECO', 'CONFORT')

```
### CLI
Ce package inclut également un utilitaire ligne de commande pour manipuler les Heatzy.

```bash
$ heatzy-cli
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
$ heatzy-cli -u login@heatzy.com -p p@ssw0rd -l                        # Liste les Heatzy
ChambreHeatzyDevice : name:Chambre,did:didbidonzzzzz,version:Pilote2,mode:OFF
SalonHeatzyDevice : name:Salon,did:didbidonxxxxx,version:Heatzy,mode:ECO
$ heatzy-cli -u login@heatzy.com -p p@ssw0rd -d Chambre                # Affiche l'info d'un heatzy
HeatzyDevice : name:Chambre,did:didbidonzzzzz,version:Pilote2,mode:OFF
$ heatzy-cli -u login@heatzy.com -p p@ssw0rd -d Bedroom -m ECO         # Change le mode du heatzy à Chambre
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
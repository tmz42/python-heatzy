import requests
import argparse

# Constantes
heatzy_api_base_url = "https://euapi.gizwits.com/app"
heatzy_appID = "c70a66ff039d41b4a220e198b0fcc8b3"

# Matrice de décodage des modes
modes_decode = {
    'Pilote2' : {'stop' : 'OFF', 'eco' : 'ECO', 'fro' : 'HGEL', 'cft' : 'CONFORT'},
    'Heatzy' : {'停止' : 'OFF', '经济' : 'ECO', '解冻' : 'HGEL', '舒适' : 'CONFORT'}
}

# Matrice d'encodage des modes
modes_encode = {
    'Heatzy' : {'OFF':{'raw':(1,1,3)},'ECO':{'raw':(1,1,1)},'HGEL':{'raw':(1,1,2)},'CONFORT':{'raw':(1,1,0)}},
    'Pilote2' : {
        'OFF':{'attrs': {'mode':'stop'}},
        'ECO':{'attrs': {'mode':'eco'}},
        'HGEL':{'attrs': {'mode':'fro'}},
        'CONFORT':{'attrs': {'mode':'cft'}}
        }
}

# Handler Heatzy : 'pont', s'authentifie auprès du serveur Gizwits et récupère le token
class HeatzyHandler:
    def __init__(self,login,password):
        self.login = login
        self.password = password
        self.token = None
        self.get_token()

    def get_token(self):
        login_headers = {'Accept': 'application/json', 'X-Gizwits-Application-Id': heatzy_appID}
        login_payload = {'username': self.login, 'password': self.password, 'lang': 'en'}
        loginRequest = requests.post(heatzy_api_base_url+'/login', json=login_payload, headers=login_headers)
        self.token = loginRequest.json()['token']
        return self.token

    # Récupère les devices
    def getHeatzyDevices(self):
        login_headers = {'Accept': 'application/json', 'X-Gizwits-Application-Id': heatzy_appID, 'X-Gizwits-User-token' : self.token}
        loginRequest = requests.get(heatzy_api_base_url+'/bindings', headers=login_headers)

        request_devices_list = loginRequest.json()['devices']
        devices_list = list()

        # Infos à extraire : device alias, did, product_name
        for device in request_devices_list:
            dev = HeatzyDevice(self,name=device['dev_alias'], did=device['did'], version=device['product_name'])
            devices_list.append(dev)

        return devices_list

# Classe HeatzyDevice
class HeatzyDevice:
    def __init__(self,handler,name,did,version):
        self.handler = handler
        self.name = name
        self.did = did
        self.version = version
        self.mode = 'UNK'
        self.status()

    # ToString
    def __str__(self):
        str = 'HeatzyDevice : name:'+self.name+',did:'+self.did+',version:'+self.version+',mode:'+self.mode
        return str

    # Rafraichit l'etat
    def status(self):
        request_headers = {'Accept': 'application/json', 'X-Gizwits-Application-Id': heatzy_appID}
        statusRequest = requests.get(heatzy_api_base_url+'/devdata/'+self.did+'/latest', headers=request_headers)

        mode = statusRequest.json()['attr']['mode']

        self.mode = modes_decode[self.version][mode]
        return self.mode

    # Définit le mode à partir du texte
    def setMode(self, mode):
        request_headers = {'Accept': 'application/json', 'X-Gizwits-Application-Id': heatzy_appID,'X-Gizwits-User-token': self.handler.token}
        request_payload = modes_encode[self.version][mode]
        setModeRequest = requests.post(heatzy_api_base_url+'/control/'+self.did, json=request_payload, headers=request_headers)

    # Méthodes de définition de modes plus lisibles
    def confort(self):
        self.setMode('CONFORT')

    def eco(self):
        self.setMode('ECO')

    def off(self):
        self.setMode('OFF')

    def horsgel(self):
        self.setMode('HGEL')

    def on(self):
        self.setMode('CONFORT')

def main():
    parser = argparse.ArgumentParser(description='Controls Heatzy devices throught the CLI')
    parser.add_argument('-u', '--username', help="Username on the Heatzy (Gizwits) platform")
    parser.add_argument('-p', '--password', help="Password of the user")
    parser.add_argument('-d', '--device', help="Name of the Heatzy device you wish to control")
    parser.add_argument('-l', '--list', help="List all devices", action="count", default=0)
    parser.add_argument('--setmode', help="Sets the mode of the device")

    args = parser.parse_args()

    # On liste les devices
    if args.list:
        hh = HeatzyHandler(args.username, args.password)
        deviceList = hh.getHeatzyDevices()

        for device in deviceList:
            print(device)

    # On définit le mode
    if args.setmode:
        pass

if __name__ == "__main__":
    main()
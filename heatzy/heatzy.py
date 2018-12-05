import requests
import time

# TODO
# Disponibilité des devices?

# Handler Heatzy : 'pont', s'authentifie auprès du serveur Gizwits et récupère le token
class HeatzyHandler:
    # Constantes
    API_BASE_URL = "https://euapi.gizwits.com/app"  # URL de base pour l'API Gizwits employée 
    APPID = "c70a66ff039d41b4a220e198b0fcc8b3"      # APPID Heatzy dans Gizwits 
    MODES_DECODE = {
        'Pilote2' : {'stop' : 'OFF', 'eco' : 'ECO', 'fro' : 'HGEL', 'cft' : 'CONFORT'}, # Modes pour Pilote2
        'Heatzy' : {'停止' : 'OFF', '经济' : 'ECO', '解冻' : 'HGEL', '舒适' : 'CONFORT'} # Modes pour Pilote Gen 1
    }
    MODES_ENCODE = {
            # Matrice d'encodage des modes pour Heatzy Pilote (Gen 1)
            'Heatzy' : {'OFF':{'raw':(1,1,3)},'ECO':{'raw':(1,1,1)},'HGEL':{'raw':(1,1,2)},'CONFORT':{'raw':(1,1,0)}},
            # Matrice d'encodage des modes pour Heatzy Pilote Gen 2
            'Pilote2' : {
                'OFF':{'attrs': {'mode':'stop'}},
                'ECO':{'attrs': {'mode':'eco'}},
                'HGEL':{'attrs': {'mode':'fro'}},
                'CONFORT':{'attrs': {'mode':'cft'}}
                }}
    MODES_AVAILABLE = ('OFF', 'HGEL',' ECO', 'CONFORT')

    # Constructeur
    def __init__(self,login,password):
        self.login = login          # Identificant
        self.password = password    # Mot de passe
        self.token = None           # Initialisation du token
        self.token_expires = None   # Timestamp d'expiration du token
        self.get_token()            # Récupération du token
        self.devices_dict = None
        self.devices_list = None

    # Récupération du token
    def get_token(self):
        # Si le token existe déjà et expire dans plus de 24h : on ne recherche pas un nouveau token
        if self.token and (self.token_expires + 86400) < time.time():
            return self.token
        
        login_headers = {'Accept': 'application/json', 'X-Gizwits-Application-Id': HeatzyHandler.APPID}     # Préparation des headers
        login_payload = {'username': self.login, 'password': self.password, 'lang': 'en'}                   # Payload du login
        loginRequest = requests.post(HeatzyHandler.API_BASE_URL+'/login', json=login_payload, headers=login_headers)

        loginJSON = loginRequest.json()
        # Si on récupère un token : OK
        if 'token' in loginJSON:
            self.token = loginJSON['token']
            self.token_expires = loginJSON['expire_at']
            return self.token

        else:
            raise Exception('Erreur de login : '+str(loginRequest.json()))

    def devices(self):
        self.getHeatzyDevices()
        return self.devices_list

    # Récupère les devices sous forme de 'Dict'
    def getHeatzyDevices(self):     # TODO : ajouter un argument refresh (défaut : false)
        # Si on n'a pas de devices, on fait la requête pour remplir les champs
        if not self.devices_list:
            login_headers = {'Accept': 'application/json', 'X-Gizwits-Application-Id': HeatzyHandler.APPID, 'X-Gizwits-User-token' : self.get_token()}
            loginRequest = requests.get(HeatzyHandler.API_BASE_URL+'/bindings', headers=login_headers)

            # TODO : Check for errors 

            request_devices_list = loginRequest.json()['devices']
            # Initialisation du dictionnaire
            devices_dict = dict()
            devices_list = list()

            # Infos à extraire : device alias, did, product_name
            for device in request_devices_list:
                dev = HeatzyDevice(self,name=device['dev_alias'], did=device['did'], version=device['product_name'])
                devices_dict[dev.name] = dev
                devices_list.append(dev)

            self.devices_dict = devices_dict         # Mise à jour des devices
            self.devices_list = devices_list
        # Dans tous les cas, on envoie les devices
        return self.devices_dict

    # TODO : ajouter méthodes de lookup by name et lookup by DID

    

# Classe HeatzyDevice
class HeatzyDevice:
    def __init__(self,handler,name,did,version):
        self.handler = handler                  # Object HeatzyHandler (pour gérer les connexions à l'API Gizwits)
        self.name = name                        # Nom du device, tel que reporté dans l'application
        self.did = did                          # Device ID (UID Gizwits)
        self.version = version                  # Version du heatzy ('Heatzy' : Gen 1, 'Pilote2': Gen 2)
        self.mode = None                        # Mode (Aucun pour l'instant)
        self.status()                           # Récupération de l'état

    # Améliorer tostring...
    # ToString
    def __str__(self):
        str = 'HeatzyDevice : name:'+self.name+',did:'+self.did+',version:'+self.version+',mode:'+self.status()
        return str

    def update(self):
        self.status()

    # Rafraichit l'etat
    def status(self):
        request_headers = {'Accept': 'application/json', 'X-Gizwits-Application-Id': HeatzyHandler.APPID}
        statusRequest = requests.get(HeatzyHandler.API_BASE_URL+'/devdata/'+self.did+'/latest', headers=request_headers)

        mode = statusRequest.json()['attr']['mode']

        # TODO : Check for errors here

        self.mode = HeatzyHandler.MODES_DECODE[self.version][mode]
        return self.mode

    # Définit le mode à partir du texte
    def setMode(self, mode):
        if mode not in HeatzyHandler.MODES_AVAILABLE:
            raise Exception('Unavailable mode : '+mode)
            
        request_headers = {'Accept': 'application/json', 'X-Gizwits-Application-Id': HeatzyHandler.APPID,'X-Gizwits-User-token': self.handler.get_token()}
        request_payload = HeatzyHandler.MODES_ENCODE[self.version][mode]
        requests.post(HeatzyHandler.API_BASE_URL+'/control/'+self.did, json=request_payload, headers=request_headers)
        # TODO : check for errors

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
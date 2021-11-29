import socket, signal, sys, random, json

from clientListener import ClientListener

class Server():
    def __init__(self, port):
        self.mots = ["pikachu", "evolie", "bulbizarre", "herbizarre", "florizarre", "salameche", "reptincel", "dracaufeu", "carapuce", "carabaffe", "tortank", "chenipan", "chrysacier",
         "papilusion", "aspicot", "coconfort", "dardargnan", "roucool", "roucoups", "roucarnage", "rattata", "rattatac", "piafabec", "rapasdepic", "abo", "arbok",
         "raichu", "sabelette", "sablaireau", "nidoran", "nidorina", "nidoqueen", "nidorino", "nidoking", "melofee", "melodelfe", "goupix", "feunard", "roudoudou", "groudoudou",
         "nosferapti", "nosferalto", "mystherbe", "ortide", "rafflesia", "paras", "parasect", "mimitoss", "aeromite", "taupiqueur", "triopikeur", "miaouss", "persian", "psykokwak",
         "akwakwak", "ferosinge", "colossinge", "caninos", "arcanin", "pitatard", "tetarte", "tartard", "abra", "kadabra", "alakazam", "machoc", "machopeur", "mackogneur", "chetiflor",
         "boustiflor", "empliflor", "tentacool", "tentacruel", "racaillou", "gravalanch", "grolem", "ponyta", "galopa", "ramoloss", "flagadoss", "magneti", "magneton", "canarticho", "doduo",
         "otaria", "lamantine", "tadmorv", "grotadmorv", "kokiyas", "crustabri", "fantominus", "spectrum", "ectoplama", "onix", "soporifik", "hypnomade", "krabby", "krabboss", "voltorbe",
         "electrode", "noeunoeuf", "noadkoko", "osselait", "ossatueur", "kicklee", "tygnon", "excelangue", "smogo", "smogogo", "rhinocorne", "rhinoferos", "leveinard", "saquedeneu",
         "kangourex", "hypotrempe", "hypocean", "poissirene", "poissoroy", "stari", "staross", "m.mime", "insecateur", "lippoutou", "elektek", "magmar", "scarabrute", "tauros",
         "magicarpe", "leviator", "Lokhlass","metamorph", "aquali", "voltali", "pyroli", "porygon", "amonita", "amonistar", "kabuto", "kabutops", "ptera", "ronflex", "artikodin",
         "electhor", "sulfura", "minidraco", "draco", "dracolosse", "mewtwo", "mew"]
        self.mot_secret = self.mots[random.randrange(0, len(self.mots))]
        self.essais_restants = 13
        self.points = 0
        self.modele_du_mot = self.str_add_spaces_between_chars("_" * len(self.mot_secret))
        self.lettres_proposees = []

        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        self.clients_sockets = []
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signal, frame):
        self.listener.close()

    def str_add_spaces_between_chars(self, str: str):
        return " ".join(str)

    def str_remove_spaces(self, str: str):
        return str.replace(' ', '')

    def run(self):
        while True:
            try:
                print("En attente de joueurs...")
                try:
                    (client_socket, client_adress) = self.listener.accept()
                except socket.error:
                    sys.exit('Connexion aux joueurs impossible')
                self.clients_sockets.append(client_socket)
                print("Start the thread for client:", client_adress)
                client_thread = ClientListener(self, client_socket, client_adress)
                client_thread.start()
            except KeyboardInterrupt:
                quit(0)

    def replacer(self, s, newstring, index, nofail=False):
        if not nofail and index not in range(len(s)):
            raise ValueError("index outside given string")
        if index < 0:
            return newstring + s
        if index > len(s):
            return s + newstring

        return s[:index] + newstring + s[index + 1:]

    def is_already_tried(self, lettre: str) -> bool:
        return lettre in self.lettres_proposees

    def remove_socket(self, socket):
        self.client_sockets.remove(socket)

    def echo(self, data: dict):
        dataToSend = json.dumps(data)
        for sock in self.clients_sockets:
            try:
                sock.sendall(dataToSend.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")

if __name__ == "__main__":
    server = Server(1234)
    server.run()

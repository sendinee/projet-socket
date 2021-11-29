from json.decoder import JSONDecodeError
import socket, threading, re, json

class ClientListener(threading.Thread):
    def __init__(self, server, socket, address):
        super(ClientListener, self).__init__()
        self.server = server
        self.socket = socket
        self.address = address
        self.listening = True

    def run(self):
        while self.listening:
            dataToSend = {
                "modele_du_mot": self.server.modele_du_mot,
                "essais_restants": self.server.essais_restants
            }

            if self.server.points == 0 and self.server.essais_restants == 13:
                self.server.echo(dataToSend)

            data = ""
            try:
                data: str = self.socket.recv(1024).decode('UTF-8')
                dataToReceive = json.loads(data)
                letter = dataToReceive["message"].lower()[0]

                if letter == "":
                    raise Exception()

                if letter in self.server.lettres_proposees:
                    dataToSend["messagebox"] = "Cette lettre a déjà été proposée..."
                else:
                    self.server.lettres_proposees.append(letter)

                    if letter in self.server.mot_secret:
                        self.server.points += self.server.mot_secret.count(letter)

                        for x in [m.start() for m in re.finditer(letter, self.server.mot_secret)]:
                            modele = self.server.str_remove_spaces(self.server.modele_du_mot)
                            nouveau_modele = self.server.replacer(modele, letter, x)
                            self.server.modele_du_mot = self.server.str_add_spaces_between_chars(nouveau_modele)
                            dataToSend["modele_du_mot"] = self.server.modele_du_mot

                        if self.server.points == len(self.server.mot_secret):
                            dataToSend["messagebox"] = "GG !!!"
                            dataToSend["endgame"] = True

                    else:
                        self.server.essais_restants -= 1
                        dataToSend["essais_restants"] = self.server.essais_restants

                        if self.server.essais_restants == 0:
                            dataToSend["messagebox"] = f"Perdu. Le mot était '{self.server.mot_secret}'."
                            dataToSend["endgame"] = True
                        else:
                            dataToSend["messagebox"] = "Faux. Il reste {0} essais.".format(str(self.server.essais_restants))
                self.server.echo(dataToSend)
            except socket.error:
                print("Unable to receive data")
            except Exception:
                continue
            except KeyboardInterrupt:
                self.listening = False
                break
            self.handle_msg(dataToReceive)

    def handle_msg(self, data: dict):
        if data["message"] == "QUIT" or data["message"] == "":
            self.listening = False
            self.socket.close()
            self.server.remove_socket(self.socket)
        else:
            self.server.echo(data)
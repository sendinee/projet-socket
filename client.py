import json, threading, socket
import re
from tkinter import *
from tkinter.messagebox import showinfo
from typing import Match

class Client():
    def __init__(self, server, port, window: Tk):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.listening = True
        self.txtvar_label_motsecret = StringVar()
        self.txtvar_label_essais = StringVar()
        self.txtvar_textfield = StringVar()
        self.txtvar_label_motsecret.set('')
        self.txtvar_label_essais.set('')
        self.txtvar_textfield.set('')
        self.label_motsecret = Label(window, textvariable = self.txtvar_label_motsecret, font = ("Helvetica", 32))
        self.label_essais = Label(window, textvariable = self.txtvar_label_essais, fg = 'red', font = ("Helvetica", 16))
        self.textfield = Entry(window, textvariable = self.txtvar_textfield)
        self.button = Button(window, text = "Essayer")
        self.button.bind('<Button-1>', self.submit_hander)
        self.label_essais.place(x = 25, y = 25)
        self.label_motsecret.place(x = 25, y = 100)
        self.textfield.place(x = 25, y = 150)
        self.button.place(x = 25, y = 200)

    def recv_data_handler(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
                maps = re.findall(r"{(.*?)}", data)

                if data != "" and len(maps) > 0:
                    for jsondata in maps:
                        dataToReceive = json.loads("{" + jsondata + "}")

                        if "essais_restants" in dataToReceive.keys():
                            self.txtvar_label_essais.set("{0} essais avant la pendaison".format(str(dataToReceive["essais_restants"])))
                        if "modele_du_mot" in dataToReceive.keys():
                            self.txtvar_label_motsecret.set(dataToReceive["modele_du_mot"])
                        if "messagebox" in dataToReceive.keys():
                            showinfo(message = dataToReceive["messagebox"])
                        if "endgame" in dataToReceive.keys():
                            exit(0)
                
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
       
    def listen(self):
        self.listen_thread = threading.Thread(target = self.recv_data_handler)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def submit_hander(self, event):
        lettre = self.textfield.get()[0].lower()
        self.txtvar_textfield.set('')
        self.send(lettre)

    def send(self, message):
        jsondumps = json.dumps({ "message": message })
        try:
            self.socket.sendall(jsondumps.encode("UTF-8"))
        except socket.error:
            print("unable to send message")
   
    def quit(self):
        self.listening = False
        self.socket.close()

    def handle_msg(self, data):
        if data == "QUIT":
            self.quit()
        elif data == "":
            self.quit()

if __name__ == "__main__":
    try:
        window = Tk()
        pendu = Client('172.16.4.32', 1234, window)
        pendu.listen()
        window.title('Pendu')
        window.geometry('400x300')
        window.mainloop()
    except KeyboardInterrupt:
        quit(0)

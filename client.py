#coding=utf-8

import socket, select, string, sys


def affiche(message) :
    sys.stdout.write(message)
    sys.stdout.flush()
 
if __name__ == "__main__":
    
    if(len(sys.argv) < 4) :
        print("Mettre: python client.py hote(adresse) port pseudo")
        sys.exit()
        
    hote = sys.argv[1]
    port = int(sys.argv[2])
    pseudo = str(sys.argv[3])
    attenteLecture = 0.05
    monbuffer = 10000

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(2)

    
    try :
        clientSocket.connect((hote,port))
    except :
        print("Connection refusé")
        sys.exit()
   
    clientSocket.send(pseudo.encode())
    
    entre = [sys.stdin, clientSocket]
    
while 1:
   
    lireSocket , ecrireSocket , erreur_socket = select.select(entre , [] , [] , attenteLecture)

    for socketTraite in lireSocket :
        
        if socketTraite == clientSocket :
            message = socketTraite.recv(monbuffer)
            message = message.decode()
            if "test EcDh492q" in message and len(message) > 13 :
                message = message.replace("test EcDh492q","")
            if not message == "test EcDh492q" :
                affiche(message)        

        else :
            message = sys.stdin.readline()
            if message :
                clientSocket.send(message.encode())

                
            
            


#coding=utf-8

import socket , select , sys , string , os


def broadcast(message) : 
    """ Renvoie le message à tous les machines excepter le serveur . """
    passage = 0
    recupMessage = 0
    if not "test EcDh492q" in message :
        recupMessage = 1
    for socketTraite in machineConnecte :
        try :
            if socketTraite != serveurSocket and socketTraite not in attentePseudo :
                socketTraite.send(message.encode())
        except :
            i = machineConnecte.index(socketTraite)
            print(" Déconnection du client sous le pseudo " + listePseudo[i])
            clientDeconnecte.append("Déconnection du client sous le pseudo " + listePseudo[i] + "\n")
            listePseudo.remove(listePseudo[i])
            machineConnecte.remove(socketTraite)
            passage = 1
            continue
    if(recupMessage) :
        print(message)
        print(listeDerniersMessage)
        listeDerniersMessage.append(message)
        print(listeDerniersMessage)
    if(passage) :
        broadcastClientDeco()
            

def broadcastClientDeco():
    """
    for socketTraite in socketDeconnecte
    broadcast(socketTraite,"Client  %s est déconnecté" % socketDeconnecte[i] )
    """
    global clientDeconnecte
    for message in clientDeconnecte :
        broadcast(message)
    clientDeconnecte = []
    
def acceptNouveauClient() :
    """ S'occuper d'accepter de nouveaux client """
    for compteur in range(0,1):
        try :
            nouveauClient , infosConnexion =  serveurSocket.accept()
            machineConnecte.append(nouveauClient)
            attentePseudo.append(nouveauClient)
            listePseudo.append("")
        except :
            print("Client refusé , serveur surchargé ? listen mis à 20 ")
            continue
    
def acceptNouveauClientWeb() :
    for compteur in range(0,1):
        try :
            nouveauClient , infosConnexion =  serveurSocketWeb.accept()
            machineConnecteWeb.append(nouveauClient)
        except :
            print("Client refusé , serveur surchargé ? listen mis à 20 ")
            continue

def traitementDesClientEnAttenteDePseudo(socketTraite) :
    """ Reçois le pseudo du client et lui permet de rejoint le chat """
    for compteur in range(0,1):
        try:
            pseudo = socketTraite.recv(monBuffer)
            if pseudo :
                pseudo = pseudo.decode()
                i = machineConnecte.index(socketTraite)
                listePseudo[i] = pseudo.rstrip('\n')
                attentePseudo.remove(socketTraite)
                broadcast("[%s] Rejoint la conversation\n" % listePseudo[i])
        except :
            listePseudo.remove(listePseudo[i])
            machineConnecte.remove(socketTraite)
            continue
            
    
def test() :
    broadcast("test EcDh492q")

def mettreAJourServeurWeb() :
    taille = len(listeDerniersMessage)
    global requete
    corps ="""
<!DOCTYPE html>
<html>
<head>
<title>Serveur Web</title>
</head>
<body>
<li>""" + listeDerniersMessage[taille-1] +  """</li>
<li>""" + listeDerniersMessage[taille-2] +  """</li>
<li>""" +  listeDerniersMessage[taille-3] +  """</li>
<li>""" +  listeDerniersMessage[taille-4] +  """</li>
<li>""" +  listeDerniersMessage[taille-5] +  """</li>
</body>
</html>"""
    tailleCorps = len(corps)
    requete = "HTTP/1.1 200 OK Content-type : text/html" + "\n" + corps
    
if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print("Mettre: python serveur.py port portMiniServeurWeb")
        sys.exit()

    requete = ""
    machineConnecte = []
    machineConnecteWeb = []
    attentePseudo = []
    listePseudo = []
    clientDeconnecte = []
    listeDerniersMessage = ["","","","",""]
    monBuffer = 4000
    port = int(sys.argv[1])
    portMiniServeurWeb = int(sys.argv[2])
    hote = ""
    hoteServeurWeb = ""
    attenteLecture = 0.05

    serveurSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serveurSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveurSocket.bind((hote,port))
    serveurSocket.listen(20)

    serveurSocketWeb = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serveurSocketWeb.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveurSocketWeb.bind((hoteServeurWeb,portMiniServeurWeb))
    serveurSocketWeb.listen(20)
   


    machineConnecte.append(serveurSocket)
    machineConnecteWeb.append(serveurSocketWeb)
    listePseudo.append('Serveur')
    print("Chat serveur demarre sur le port ", str(port))
    
    while 1 :
        lireSocket , ecrireSocket , erreur_socket = select.select(machineConnecte , [] , [] , attenteLecture)
        lireSocketWeb , ecrireSocketWeb , erreur_socketWeb = select.select(machineConnecteWeb , [] , [] , attenteLecture)
        

      
        for socketTraite in lireSocket :
            test()
            
            if socketTraite == serveurSocket :
                acceptNouveauClient()

            elif socketTraite in attentePseudo :
                traitementDesClientEnAttenteDePseudo(socketTraite)
 
            else :
                try :
                    try:
                        i  = machineConnecte.index(socketTraite)
                    except :
                        pass
                    message = socketTraite.recv(monBuffer)
                    if message :
                        message = '{' + listePseudo[i] + '} ' + message.decode()
                        broadcast(message)
                except :
                    i = machineConnecte.index(socketTraite)
                    broadcast("Déconnection du client sous le pseudo " + listePseudo[i] )
                    print(" Déconnection du client sous le pseudo " + listePseudo[i])
                    listePseudo.remove(listePseudo[i])
                    machineConnecte.remove(socketTraite)
                    continue

        for socketTraite in lireSocketWeb :
            mettreAJourServeurWeb()
            if socketTraite == serveurSocketWeb  :
                acceptNouveauClientWeb()
            else :
                try:
                    message = socketTraite.recv(monBuffer)
                    message = message.decode() # Traiter les erreurs du serveur web?
                    requete = requete.encode()
                    socketTraite.send(requete)
                    machineConnecteWeb.remove(socketTraite)
                    socketTraite.close()
                
                except : 
                    machineConnecteWeb.remove(socketTraite)
                    continue

    serveurSocket.close()
    



# Introduction à la sécurité des protocoles réseaux

## Rappel de l'objectif

L'objectif de ce TP est d'approfondir nos connaissances sur le comportement des piles TCP/IP de différentes OS. Afin de mener à bien ce TP, il est important de visualiser les trames qui circulent sur le réseau, de les analyser et de forger nos propres paquets.

Le but du TP est de de nous faire prendre conscience de ce que l'on peut voir et faire au niveau des couches 2, 3 et 4.

## Environnement

## Rappel théoriques sur TCP/IP

**Expliquez en détail le fonctionnement d'une connexion sur un port UDP. Illustrez vos propos en
capturant les trames émises lors d'une requête DNS. Vous pourrez par exemple utiliser la
commande nslookup.**

Le protocole UDP est un protocole orienté transaction et non connexion. Lors de l'utilisation du protocole UDP, les données sont envoyées sans établir de connexion avec le récepteur. UDP ne peut donc garantir que les données vont arriver. Cependant cela permet de transmettre des données de façon très simple. On envoi et c'est tout, on ne s'occupe pas de savoir si c'est bien arrivé.

Lors d'une communication UDP entre deux machines, les entités sont définies par une adresse IP et un numéro de port. La connexion sur un port est très basique. Soit le port est ouvert et le message passe, soit le port est fermé et le message ne passe pas.

Dans le cas où le port est ouvert le message est transmis et la machine émettrice ne reçoit aucun retour, cela veut dire que la connexion a été établie. Dans le cas contraire, si le port est fermé la machine émettrice reçoit un paquet ICMP contenant le message d'erreur.

```bash
sudo nmap -sU 192.168.9.133 -p 991
```

```bash
sudo nmap -sU google.fr -p 991
```

**Expliquer en détail le fonctionnement d'une connexion sur un port TCP. Illustrez vos propos en
capturant les trames émises lors d'une requête HTTP sur un site de votre choix. Pour cela vous
ne devrez pas passer par votre navigateur Web. Donnez le détail de la(es) commande(s) que
vous avez utilisé pour cette requête.**

Le protocole TCP est un protocole orienté connexion et non transaction. Ce protocole de transport est bien plus fiable que UDP. Dans le modèle OSI le protocole TCP correspond à la couche de transport.

La connexion TCP se déroule en trois phases. La première est l'établissement de la connexion. La seconde est le transferts de données et la dernière est la fin de la connexion. Par rapport à UDP le transport des données est fiable et de nombreux mécanismes permettent de garantir le bon déroulement du transfert ou alors de connaitre la cause des problèmes.

L'établissement d'une connexion TCP entre deux hôtes se déroule selon un handshaking en trois temps. Le 3 Way Handshake. Ce dernier se déroule donc en trois phases :
* SYN : Afin d'établir une connexion, le client envoie un paquet SYN (synchronized) au serveur.
* SYN / ACK : Le serveur répond au client avec un paquet SYN / ACK (synchronized, acknowledge).
* ACK : Pour terminer la connexion, le client envoie un paquet ACK au serveur au titre d'accusé de réception.


Reference-style:
![alt text][ping]

[ping]: https://github.com/DIVINIX/Scapy/blob/master/ping.PNG "Ping image"

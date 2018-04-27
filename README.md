# Introduction à la sécurité des protocoles réseaux

## Rappel de l'objectif

L'objectif de ce TP est d'approfondir nos connaissances sur le comportement des piles TCP/IP de différentes OS. Afin de mener à bien ce TP, il est important de visualiser les trames qui circulent sur le réseau, de les analyser et de forger nos propres paquets.

Le but du TP est de de nous faire prendre conscience de ce que l'on peut voir et faire au niveau des couches 2, 3 et 4.

## Infrastructure de travail

L'infrastructure  de travail est composée de la manière suivante :
* Une machine hôte d'IP `192.168.8.53` sous Windows
* Une machine attaquant d'IP `192.168.9.132` et d'adresse MAC `08:00:27:9f:ae:7e` sous Ubuntu Server 16.04
* Une machine cible d'IP `192.168.9.133` et d'adresse MAC `08:00:27:5a:52:a1` sous Ubuntu Server 16.04

## Rappels théoriques sur TCP/IP

### 1. UDP

**_Expliquez en détail le fonctionnement d'une connexion sur un port UDP. Illustrez vos propos en
capturant les trames émises lors d'une requête DNS. Vous pourrez par exemple utiliser la
commande nslookup._**

Le protocole UDP est un protocole orienté transaction et non connexion. Lors de l'utilisation du protocole UDP, les données sont envoyées sans établir de connexion avec le récepteur. UDP ne peut donc garantir que les données vont arriver. Cependant cela permet de transmettre des données de façon très simple. On envoi et c'est tout, on ne s'occupe pas de savoir si c'est bien arrivé.

Lors d'une communication UDP entre deux machines, les entités sont définies par une adresse IP et un numéro de port. La connexion sur un port est très basique. Soit le port est ouvert et le message passe, soit le port est fermé et le message ne passe pas.

Dans le cas où le port est ouvert le message est transmis et la machine émettrice ne reçoit aucun retour, cela veut dire que la connexion a été établie. Dans le cas contraire, si le port est fermé la machine émettrice reçoit un paquet ICMP contenant le message d'erreur.

Afin de mettre en avant le principe d'une connexion UDP, on peut par exemple utiliser la commande `nmap`. Nmap est un scanner de port. Il permet notamment de déterminer si un port est ouvert ou non.

Avec cette commande je vais donc tester l'ouverture d'un port sur différentes cibles. Dans un premier temps je vais tester l'ouverture du port TCP/UDP 991 chez Google avec la commande suivante :

```console
sudo nmap -sU google.fr -p 991
```

Le résultat de la commande est le suivant :

![alt text][udp_open_nmap]

[udp_open_nmap]: https://github.com/DIVINIX/Scapy/blob/master/Images/udp_open_nmap.PNG "UDP port open nmap"

On remarque bien que le port est ouvert, c'est la ligne `991/udp open|filtered unknown` qui le confirme. De plus on peut vérifier le déroulement de la connexion dans **Wireshark** et on voit bien que les paquetes ont bien été envoyé.

![alt text][udp_open_wireshark]

[udp_open_wireshark]: https://github.com/DIVINIX/Scapy/blob/master/Images/udp_open_wireshark.PNG "UDP port open wireshark"

Dans un second temps je vais tester le même port mais sur la machine virtuelle victime. La commande est la même, seul l'adresse cible change :

```console
sudo nmap -sU 192.168.9.133 -p 991
```
Le résultat de la commande est le suivant :


![alt text][udp_close_nmap]

[udp_close_nmap]: https://github.com/DIVINIX/Scapy/blob/master/Images/udp_close_nmap.PNG "UDP port close nmap"

Cette fois ci on remarque que le port est fermé grâce à la ligne `991/udp closed unknown`. La vérification dans Wireshark le confirme, la cible nous retourne un paquet ICMP avec le message `Port unreachable`.

![alt text][udp_close_wireshark]

[udp_close_wireshark]: https://github.com/DIVINIX/Scapy/blob/master/Images/udp_close_wireshark.PNG "UDP port close wireshark"

### 2. TCP

**_Expliquer en détail le fonctionnement d'une connexion sur un port TCP. Illustrez vos propos en
capturant les trames émises lors d'une requête HTTP sur un site de votre choix. Pour cela vous
ne devrez pas passer par votre navigateur Web. Donnez le détail de la(es) commande(s) que
vous avez utilisé pour cette requête._**

Le protocole TCP est un protocole orienté connexion et non transaction. Ce protocole de transport est bien plus fiable que UDP. Dans le modèle OSI le protocole TCP correspond à la couche de transport.

La connexion TCP se déroule en trois phases. La première est l'établissement de la connexion. La seconde est le transfert de données et la dernière est la fin de la connexion. Par rapport à UDP le transport des données est fiable et de nombreux mécanismes permettent de garantir le bon déroulement du transfert ou alors de connaitre la cause des problèmes.

L'établissement d'une connexion TCP entre deux hôtes se déroule selon un handshaking en trois temps. Le 3 Way Handshake. Ce dernier se déroule donc en trois phases :
* SYN : Afin d'établir une connexion, le client envoie un paquet SYN (synchronized) au serveur.
* SYN / ACK : Le serveur répond au client avec un paquet SYN / ACK (synchronized, acknowledge).
* ACK : Pour terminer la connexion, le client envoie un paquet ACK au serveur au titre d'accusé de réception.

Pour démontrer le fonctionnement de TCP et son **3 Way Wandshake**, j'ai effectué une requête HTTP avec la commande ``curl``. 

```console
curl dreamzite.com -p 443
```

Le résultat de cette commande peut être capturé dans Wireshark. On voit donc le déroulement du **3 Way Handshake**.

![alt text][tcp_wireshark]

[tcp_wireshark]: https://github.com/DIVINIX/Scapy/blob/master/Images/tcp_synack_wireshark.PNG "TCP wireshark"

## Utilisation de scapy

### 1. Découverte de l'outil

**_Suivez le tutoriel officiel pour prendre en main l'outil. Concentrez-vous uniquement sur les
paragraphes suivants de la partie usage, tout le paragraphe Interactive tutorial jusqu'à
Send and receive in a loop inclu. Pour tester, forgez quelques paquets, capturez les trames
et observez le résultat. Décrivez vos manipulations._**

Les parties antérieures à la génération de paquets sont très basiques. Je ne les expliquerais donc pas dans les manipulations pour la découverte de scapy.

#### a. Generating sets of packets
  
Scapy permet la génération de plusieurs paquets très facilement. Ci-dessous se trouve le résultat de la génération de paquets :

![alt text][set_packets]

[set_packets]: https://github.com/DIVINIX/Scapy/blob/master/Images/set_packets.PNG "Generating packets"

L'un des avantages est de pouvoir forger un certain nombre de paquets de manière automatique. Par exemple ici l'idée était de forger des paquets TCP de différents ports pour différentes adresses. Dans un premier temps récupère les adresses IP de la cible. Ensuite on créer une trame TCP pour les ports 80 et 443. Pour finir on génère automatiquement les paquets associés aux IP et aux ports TCP. Cela nous donne des paquets de la forme : Adresse IP 1 + Port 80 | Adresse IP 1 + Port 443 | Adresse IP 2 + Port 80 | Adresse IP 2 + Port 443 [...]. Pour chaque adresse IP on lui associe un des deux ports de la trame TCP.

#### b. Send and receive packets (sr)
  
Les commandes `send()` et `sendp()` ne permettent pas de récupérer de retour, en effet elles ne servent qu'à envoyer. C'est pourquoi il existe des commandes comme `srp()`, `sr` et `sr1()` qui retournent des paquetes. Les deux premières fonctions retournent deux objets, le premier contient les paquets émis et leur réponses et l'autre paquet contient les paquets sans réponse. La commande `sr1()` ne retourne que les paquets émis.

L'envoi de paquets est très simple il se fait de la manière suivante : `p = sr1(IP(dst="www.slashdot.org")/ICMP()/"XXXXXXXXXXX")`

Le résultat est le suivant :

![alt text][sr_packets]

[sr_packets]: https://github.com/DIVINIX/Scapy/blob/master/Images/sr_cmd.PNG "Send and receive packets"

On voit bien que le paquet a été envoyé et qu'une réponse nous est retournée.

#### c. SYN Scans

Scapy permet entre autres de scanner un port afin de savoir s'il est ouvert. Le principe est simple, on envoie un paquet SYN sur un port pour connaitre son état. Cette opération peut être réaliser à l'aide de la commande suivante : `sr1(IP(dst="google .fr")/TCP(dport=80,flags="S"))`

Le résultat est le suivant :

![alt text][syn_scan]

[syn_scan]: https://github.com/DIVINIX/Scapy/blob/master/Images/sr_cmd.PNG "Syn Scan"

Le retour nous montre bien qu'un paquet avec un flag **SY** pour Syn-Ack nous est renvoyé. Cela veut dire que le port est bien ouvert.

#### d. Sniff and filters
  
Il est possible d'écouter ce qui se passe sur le réseau. Grâce au `sniff()` de Scapy on peut par exemple savoir les paquets qui ont été échangé sur le réseau. Il est intéressant d'associer le `sniff()` avec des filtres.
Par exemple j'ai lancé le sniff avec comme filtre l'IP de l'attaquant grâce à la commande suivante : `sniff(filter="icmp and host 192.168.9.132", count=2)`. Ensuite j'ai simplement effectué un **ping** sur l'attaquant.

Le résultat est le suivant :

![alt text][sniff_ping]

[sniff_ping]: https://github.com/DIVINIX/Scapy/blob/master/Images/sniff_ping_2.PNG "Sniff ping"

On voit bien que deux paquets on été sniffé par Scapy.


#### e. Send and receive in a loop

### 2. Réalisation d'une connexion TCP

**_Vous forgerez des trames TCP afin de réaliser de bout en bout une connexion 3
Way handshake. Pour cela vous pourrez capturer une connexion TCP pour
visualiser en détail comment se positionnent les options._**

Dans le but d'établir une connexion TCP et de mettre en avant le **3 Way Handshake**  j'ai effectué un sniff sur des trames TCP. L'idée était donc d'avoir d'un côté des trames TCP et de l'autre de sniffer ces trames à l'aide de scapy.
J'ai donc créé un fichier Python qui gère la création d'une trame TCP et qui gère aussi son envoi.
Ci-dessous se trouve le contenu de ce fichier python :

```python
#!usr/bin/env python
from scapy.all import *

sr1(IP(dst="dreamzite.com")/TCP(dport=443, flags="S"))
send(IP(dst="dreamzite.com")/TCP(dport=443, flags="A"))
```

L'idée était donc de lancer le sniff de l'adresse cible avec scapy et ensuite d'exécuter le script python. La commande pour le sniff de scapy est la suivante :`sniff(filter="host 54.37.226.47", count =5)`. Au moment de l'exécution du script, le sniff étant lancé il capture naturellement les trames. Voici le résultat obtenu avec scapy :

![alt text][tcp_sniff]

[tcp_sniff]: https://github.com/DIVINIX/Scapy/blob/master/Images/sniff_TCP.PNG "TCP sniff"

On peut remarquer que la connexion **3 Way Handshake** est bien présente. Dans un premier temps la machine source d'IP '192.168.9.132' envoi une requête avec le flag "S" pour Syn. Dans un second temps la cible `54.37.226.47` lui répond avec le flag "SA" pour Syn-Ack. Enfin la source répond à la cible avec un flag "A" pour Ack.

Il est aussi possible de voir le même déroulement sur Wireshark :

![alt text][tcp_sa]

[tcp_sa]: https://github.com/DIVINIX/Scapy/blob/master/Images/syn_ack_TCP.PNG "TCP sa"

On remarque bien les trames TCP **SYN** et **ACK** envoyé par la source à la cible. Il manque juste la réponse de la cible dû à un problème de filtre.

### 3. ARP cache poisonning

**_Tentez de monter cette attaque contre une de vos machines. Pour cela vous
forgerez vous même les trames ARP, et n'utiliserez pas les fonctions automatiques
intégrées à Scapy. Expliquez en détail comment vous avez fait._**

#### a. Forger quelques trames ARP

Le principe du protocole **ARP** est de retrouver une adresse **MAC** à partir d'une adresse **IPV4**. Scapy nous permet de le faire très simplement. Il y a différentes façons de le faire. Ci-dessous se trouve deux façons différentes, la première consiste en une simple trame ARP et la seconde ressemble beaucoup à la première mais la trame comporte une partie Ethernet en plus.

```python
#!usr/bin/env python
from scapy.all import *

print("ARP sans ethernet")                                                                                           
rep, non_rep = sr(ARP(op=ARP.who_has, psrc="192.168.9.132", pdst="192.168.9.133"))
rep.show()

print("ARP avec ethernet sur cible")
rep, non_rep = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=ARP.who_has, psrc="192.168.9.132", pdst="192.168.9.133"))
rep.show()

print("ARP avec ethernet sur dreamzite")
rep, non_rep = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=ARP.who_has, psrc="192.168.9.132", pdst="192.168.8.53"))
rep.show()

```

Les trames sont assez simples. On définit l'adresse de la source et l'adresse cible dont on veut connaitre l'adresse MAC.
Le résultat de l'exécution du script est le suivant :

![alt text][arp]

[arp]: https://github.com/DIVINIX/Scapy/blob/master/Images/arp_ssh.PNG "ARP"

On voit bien que la résolution d'adresse a bien fonctionné. La machine cible a bien pour adresse `08:00:27:5a:52:a1`, la deuxième cible est la machine hôte des machines virtuelles.

#### b. Expliquer la technique de ARP cache poisonning
#### c. Monter une attaque ARP cache poisonning

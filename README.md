# spotifree-grp2
developpement application Spotifree - Groupe 2

Voir les issues sur le GIT pour ce qu'il reste à faire / améliorer 

172.17.0.2  spotifree_mariadb       sql dabase
172.17.0.3  archlinux_loup          sshd server
172.17.0.4  spotifree_ftp           ftp m

Installation
1 - creer un dossier Spotifree dans un repertoire personnel. Ce fichier servira a la fois pour placer les fichiers de configurations (si requis, ex clé RSA) et servira egalement de lieux de dépot des musiques ecoutées.

2 - création des 3 dockers

2-1 Docker CORE ssh :
archlinux_remake.dockerfile
copier le script spotifree_core.sh sur le docker CORE

core : 
user jenkins
> passwd jenkins
mdp : jenkins
sudo pacman -S mariadb # pour permettre de lancer les commandes mysql dans le script spotifree_core.sh

2-2 Docker Mariadb SQL :
sudo docker run --detach --name spotifree_mariadb --env MARIADB_USER=spotifree_user --env MARIADB_PASSWORD=user --env MARIADB_ROOT_PASSWORD=root  mariadb:latest

mysql -h 172.17.0.2 -u spotifree_user  -puser base_de_donnees < fichier_dump
sudo docker exec -it spotifree_mariadb bash

utilisateur mariadb
user : spotifree_user
mdp : user


2-3 Docker FTP (stockage musique)
sudo docker run -d --name=spotifree_ftp -p 219:21 -p 21000-21010:21000-21010 -e USERS="ftp_spotifree|spotifree|/home/" -e ADDRESS=ftp.spotifree.com delfer/alpine-ftp-server

connecter via filezilla :
filezilla ftp://ftp_spotifree:spotifree@ftp.spotifree.com/home/first_try/

lancer en terminal :
ftp ftp_spotifree@ftp.spotifree.com

lancer le docker :
sudo exec -it spotifree_ftp sh

recrer cette architecture avec filezilla par exemple
location="/home/ftp_user/general/Queen_I_Want_to_Break_Free.mp3"
copier les musiques dans le dossier /home/ftp_user/general/ présentes sur le git dans le dossier ftp_spotifree

3 - Architecture de la base de donnés MariaDB (SQL)
Voir fichier docker_sql_architecture.odt

4 - Lancement du programme
Le client lance le script avec la commande : python spotifree_client.py
1er choix : créer un nouvel utilisateur / se connecter avec un utilisateur existant
Vérification dans la BDD SQL table users
Menu choix : 
1/ Recherche de musique
2/ Playlists (TO DO)
3/ Spotifriends (TO DO)

Recherche de musique :
1/ Recherche par mot clef
2/ Afficher toutes les musiques

Recherche par mot clef :
Cherche le mot entrer par l'utilisateur dans la table songs, colonnes title, artist, album.
Affiche la liste des musqiues matchant sur la recherche (ou toutes).

Sélection d'une musique (avec l'id_song). Récupère la location du fichier dans la table song, colonne file_location.
Découpe cette information pour avoir le nom du fichier et le chemin d'accès.
Connection au docker ftp et télécharge la musique correspondante ou l'utilisateur se trouve côté client.
Lance la musique avec le module playsong.

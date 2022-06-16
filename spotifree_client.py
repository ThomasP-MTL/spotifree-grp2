#!/usr/bin/env python3

# script spotifree côté client
# date : semaine du 13 juin 2022
# auteurs : Thomas P, Guillaume B
# lancement : python spotifree_client.py

################################################################
# DESCRIPTION - ETAT D'AVANCEMENT
################################################################
# le script gere la connexion ssh vers le docker Core
# il permet de creer un utilisateur
# la connexion verifie le combo user + password present dans la table users du docker SQL
# il permet de rechercher une chanson; par mot clé ou par affichage de liste
# l'utilisateur choisit une chanson et l ecoute ou    [ l ajoute a une playlist (PARTIE A FAIRE)]
# L ecoute de la chanson declenche le téléchargement du fichier à partir du docker FTP (lien récupéré dans le docker SQL) 
# dans le dossier courant et lance la lecture. L utilisateur perd la main durant le temps de la chanson.



################################################################
# Importation des modules
################################################################

# import ...
import ftplib
# from ftplib import FTP
import subprocess
import os
from playsound import playsound 
################################################################
# Declaration des variables de connexion
################################################################

# parametres connexion ssh docker core

###commande de connexion 
ssh = "ssh -t jenkins@172.17.0.3" 

# parametres connexion ftp (https nginx proxy ftp plus tard) docker
# ftp-terminal = "ftp ftp_spotifree@ftp.spotifree.com"

###statut de connection: si =0 user+pwd OK si =1 connexion refusée
conn_status=-1



################################################################
# Definition des classes
################################################################


################################################################
# Definition des fonctions
################################################################
# def download_song(location):
#     ftp = FTP('ftp.spotifree.com', 'ftp_spotifree', 'spotifree')  # connect to host, default port
#     print(location)


# intéressant de créer toutes ces fonctions ???

# fonctions permettant d'ajouter à la bdd sql
# def add_bdd_user
# def add_bdd_friend
# def add_bdd_message
# def add_bdd_playlist
# def add_bdd_song_to_playlist
# def add_bdd_user_to_playlist

# fonctions permettant de supprimer à la bdd sql
# def rm_bdd_friend
# def rm_bdd_playlist




################################################################
# Script 
################################################################

# login & mdp
# 2 choix : 


### on laisse l utilisateur dans la boucle tant que la connexion n'est pas autorisée (user+pwd valide)
while conn_status != "0":
    connect_mode=input("Souhaitez vous vous connecter à l'aide d'un compte existant ou créer un nouvel utilisateur ?  (1/2)")
    
    if connect_mode == "1":
        user=input("entrez votre nom d'utilisateur : ")
        password=input("entrez le mot de passe : ")
        ### execute la connection au docker Core via ssh puis execute la fonction connexion du script core
        ### subprocess.run(["ssh", "jenkins@172.17.0.3", "bash spotifree_core.sh"+" "+"connexion"+" "+user+" "+password])
        ###idem ci dessus mais enregistre l'output en binaire de la commande dans une variable (TOUT l'output, incluant le /n de fin de ligne)
        conn_status=subprocess.check_output(["ssh", "jenkins@172.17.0.3", "bash spotifree_core.sh"+" "+"connexion"+" "+user+" "+password]).decode().split("\n")[0]
        print(conn_status)
        ### on pourrait faire un test si user existe et mauvais mdp ou si user n existe pas, pour donner des retours plus précis à l user
    elif connect_mode == "2":
        new_user=input("entrez votre nom d'utilisateur : ")
        new_password=input("entrez le mot de passe : ")
        arg1="add_user"
        subprocess.run(["ssh", "jenkins@172.17.0.3", "bash spotifree_core.sh"+" "+arg1+" "+new_user+" "+new_password])
        conn_status=subprocess.check_output(["ssh", "jenkins@172.17.0.3", "bash spotifree_core.sh"+" "+"connexion"+" "+user+" "+password]).decode().split("\n")[0]
        print(conn_status)
    else :
        print("Mauvaise entrée! seuls les reponses \"1\" ou \"2\" sont valides")   
    
    ### boucle infinie tant que l'user ne se connecte pas ou ne crée pas un user..
    # print(conn_status)


### application
### menu choix
print("##### Menu d'options #####")
print("Choix 1 : recherche une chanson")
print("Choix 2 : gestion des playlists")
print("Choix 3 : Spotifriend")


x=int(input("Que voulez vous faire ? (1/2/3)"))

### cascade de boucle if selon les choix de l'utilisateur

### recherche de chansons
if x == 1:
    print("choix 1")
    print("Parametre de recherche : ")
    print("Choix 1 : recherche par mot clé")
    print("Choix 2 : afficher les musiques")
    x1=int(input("Que voulez vous faire ? (1/2)   "))
    ### recherche par mot clé
    if x1 == 1:
        # print("choix x1_1")
        keyword=input("entrez le mot clé de la recherche : ")
        #subprocess :  puis connexion ssh au docker Core puis requete SQL au docker SQL pour chercher dans la table des musiques
        subprocess.run(["ssh", "jenkins@172.17.0.3", "bash spotifree_core.sh"+" "+"search_keyword"+" "+keyword])
        ### selection de la musique
        x1_1_1=input("Selectionnez l ID d une chanson")
        ### choix d action
        x1_1_2=int(input("voulez vous l' ecouter ou l ajouter a une playlist ?  (1/2) "))
        ### ecoute de la musique selectionnée
        if x1_1_2 == 1:
            ### telecharger la musique. ######## on telecharge la musique dans le dossier d'ou le programme est lancé
            song_location=subprocess.check_output(["ssh", "jenkins@172.17.0.3", "bash spotifree_core.sh"+" "+"location"+" "+x1_1_1]).decode().split("\n")[1]
            
            ### cheat
            # location="/home/ftp_user/general/Queen_I_Want_to_Break_Free.mp3" 
            
            # download_song(ftp, location)  #### essai fonction
            filename = song_location.rsplit("/", maxsplit=1)[1] 
            print ("Téléchargement de la musique : ",filename) 
            ### split en partant de la droite, fait UN split, et on affiche le segment [0] en partant de la gauche
            pathway = song_location.rsplit("/", maxsplit=1)[0]
            # print ("pathway = ", pathway)
            ### connexion au docker ftp
            with ftplib.FTP('ftp.spotifree.com', 'ftp_spotifree', 'spotifree') as ftp:
                ftp.cwd(pathway)
                with open(filename, 'wb') as f:
                    ftp.retrbinary('RETR ' + filename, f.write)
                    ftp.close()
            ### ecouter : on n'a aucun controle sur la lecture qui continu jusqu'a la fin de la chanson
            playsound(filename)
            #  os.spawnl(os.P_NOWAIT, playsound(filename))
            
        elif x1_1_2 == 2:
            ### ajout playlist
            pass
    ### affichage complet de la table chanson #### LECTURE ALEATOIRE ??    
    elif x1 == 2:
        #print("choix x1_2")
        ### subprocess : connection ssh au docker core puis requete sql au docker sql qui affiche la table songs au complet
        subprocess.run(["ssh", "jenkins@172.17.0.3", "bash spotifree_core.sh"+" "+"show_songs"])
        ### selection de chanson
        x1_2_1=input("Selectionnez l ID d une chanson")
        ### choix d action
        x1_2_2=int(input("voulez vous l' ecouter ou l ajouter a une playlist ?  (1/2) "))
        ### ecoute de la chanson 
        if x1_2_2 == 1:
            #telecharger la musique. ###### on le fait 2 fois ->>>> fonction jusqua ftp.close()
            song_location=subprocess.check_output(["ssh", "jenkins@172.17.0.3", "bash spotifree_core.sh"+" "+"location"+" "+x1_2_1]).decode().split("\n")[1]
            filename = song_location.rsplit("/", maxsplit=1)[1] 
            print ("Téléchargement de la musique : ",filename) 
            #split en partant de la droite, fait UN split, et on affiche le segment [0] en partant de la gauche
            pathway = song_location.rsplit("/", maxsplit=1)[0]
            # print ("pathway = ", pathway)
            with ftplib.FTP('ftp.spotifree.com', 'ftp_spotifree', 'spotifree') as ftp:
                ftp.cwd(pathway)
                with open(filename, 'wb') as f:
                    ftp.retrbinary('RETR ' + filename, f.write)
                    ftp.close()
            playsound(filename)
            # os.spawnl(os.P_NOWAIT, playsound(filename))
        ### ajout de la chanson selectionné a une playlist
        elif x1_2_2 == 2:
            #ajout playlist ###### on le fait 2 fois ->>>> fonction
            pass  
    else :
        print("je ne comprends pas")
        
### Section Playlist    
elif x == 2:
    print("choix 2")
    
    # 2) playlists (table playlists)
    # - voir playlists de l'user et celles que ces amis lui ont partagé
    # - ajouter / supp des playlists
    # - écouter une playlist (boucle python sur les songs de la playlist), les télécharge et lance l'écoute
    
### Section Spotifriends
elif x == 3:
    print("choix 3")
    # 3) spotifriends (table spotifriends)
    # - voir liste d'amis
    # - ajout / supp amis (affiche les utilisateurs présents dans la table users ?)
    # - envoyer msg --> table messages
    # - partage de playlist : affiche playlist de l'utilisateur et liste d'amis

else :
    print("je ne comprends pas")
    


 



#### gestion du menu par case au lieu de boucle if
# def f(x):
#     match x:
#         case 'a':
#             return 1
#         case 'b':
#             return 2
#         case _:
#             return 0   # 0 is the default case if x is not found
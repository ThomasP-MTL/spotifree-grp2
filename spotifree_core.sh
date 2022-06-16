#!/bin/bash

# script spotifree côté serveur
# date : semaine du 13 juin 2022
# auteurs : Thomas P, Guillaume B
# lancement : bash spotifree_core.sh

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# IMPORTANT : PLACER LE SCRIPT AU BON ENDROIT DANS LE DOCKER AVEC LE DOCKERFILE
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

####################################
# le script est capable de recuperer les arguments du script Python client à l interieur du docker Core. Le 1er argument definit la fonction appelée dans le script, les arguments suivant sont utilisés pour la fonction appelée.
#Les requetes SQL sont fonctionnelles, le programme interagit avec le Docker SQL puis affiche/renvoie les données vers le client
####################################



###### declarer les variables
#utiliser pour confirmer si le combo id + password existe
check=0 
#variable de connection au Docker SQL pour alleger le text
mysql="mysql -h 172.17.0.2 -u spotifree_user -puser db_spotifree -e"



###### declarer les fonctions



### pour recuperer les infos
#le script python client  se connecte en ssh et run le script avec des arguments: on parcourt les arguments dans la fonction main
# on aurait toujours 3 arguments : type de fonction (select, insert, etc) - liste des tables impactees - nom des colonnes


### connexion au docker SQL qui contient les tables

#modifier le show tables' par la directive souhaitée en fonction des parametres recus du script client
#$mysql 'show tables;'

# -B retire le formatage table, enleve les encadrements
#$mysql 'show tables;' -B


### creation d un utilisateur
function add_user(){
  #echo "dans la fonction add_user"  
  ###--- VOIR LIGNE 23 variable mysql qui permet la connection au docker SQL
  $mysql  'INSERT INTO users (username, password) VALUES ("'$1'", "'$2'");' 
  #$mysql  'SELECT * FROM users;'
}

### supression d un user
function remove_user(){
  $mysql  'DELETE FROM users WHERE username = "'$1'";' 
  #$mysql  'SELECT * FROM users;'
}

### verification des credentials de connexion : combo user+password
function check_credents (){
    ### grep 1 : si un seul combo user+pwd est retourné, la connexion est validé
    $mysql 'SELECT count(*) FROM users WHERE username = "'$1'" AND password = "'$2'";' | grep "1" >/dev/null
    # echo "le code de sortie est $?"
    ### il faudrait trouver un moyen sans faire de echo... mais dans spotifree_client.py on execute subprocess.check_output . Si il n y pas de retour (output) il n y a rien a checker..
     if [[ $? -eq 0 ]]
         then echo "0"
	#     conn_sucess="success"
     else
    #     #on pourrait faire un test si user existe et mauvais mdp ou si user n existe pas, pour donner des retours plus précis à l user
         echo "1"
     fi
    # echo $conn_success > conn_status.log
}  

  
# faire une boucle dans le prog python client pour redemander le combo user+passwd  OU si on doit creer le user

### fonction qui retourne le chemin d'acces de la musique donné en argument (a l aide du id_song, UNIQUE)
function location() {
$mysql 'SELECT file_location FROM songs WHERE id_song = "'$1'";'
}
### fonction qui affiche la table song au compler
function show_songs() {
$mysql 'SELECT id_song, title, album, artist FROM songs;'   
}
### fonction qui recherche un mot clé dans la table song
function search_songs() {
$mysql 'SELECT id_song, title, album, artist FROM songs WHERE title LIKE "%'$1'%" OR album LIKE "%'$1'%" OR artist LIKE "%'$1'%";'   
}

### fonction principale
### le 1er argument $1 sert a selectionner la fonction a appeler, les arguments suivants sont les arguments de la fonction appelée
function main(){
    #echo "liste d argument, $@" 
    ############ faire des conditions d appel de fonctions, en fonction du  1er argument recu
    if [[ "$1" == "add_user" ]] ; then
	    # attention verifier si l utilisateur existe avant de le créer pour ne pas faire de doublons (dans table users mettre username en UNIQUE ?)    
         add_user $2 $3
    elif [[ "$1" == "connexion" ]] ; then
	 check_credents $2 $3
    elif [[ "$1" == "show_songs" ]] ; then
        show_songs
    elif [[ "$1" == "search_keyword" ]] ; then
        search_songs $2
    elif [[ "$1" == "location" ]] ; then
	location $2
    fi

    

    # add_user $2 $3
    #remove_user $1
    

    
    #test
    
    
    
    # echo "$#"
    # if [[ $# -eq 1 ]] ; then
    #     loginFile=$1
    # elif [[ $# -eq 3 ]] ; then
    #     testuserfc $1 $2 $3
    #     return
    # else
    #     saisirFile
    # fi
    # lirefichier $loginFile
}

main "$@"

#!/bin/bash

#####################################################################
#                                                                   #
#       Ce script permet d'ajouter un utilisateur à un groupe samba #
#       Utilisation : ./add_smb utilisateur groupe                  #
#                                                                   #
#                                                                   #
#####################################################################

#On sauvegarde la conf
cp -v /etc/samba/smb.conf ~/smb.conf.bak

#On récupère le numéro de ligne du groupe dans lequel on veut ajouter l'utilisateur
tmp_l=$(grep -in $2 test.conf | cut -d':' -f 1 | head -n 1)

if [ -z $tmp_l ]; then
    echo "Groupe non trouvé..."
    exit 1
fi

#On récupère le numéro de ligne des "valid users" de ce groupe
line=$(tail -n +$tmp_l test.conf | grep -in users | cut -d':' -f 1 | head -n 1)

if [ -z $line ]; then
    echo "Pas de liste d'utilisateurs autorisés dans le groupe";
    exit 1
fi

let "line=$line+$tmp_l-1"

#On vérifie que l'utilisateur n'est pas déjà dans le groupe
cat test.conf | head -n $line | tail -n 1 | grep $1 >> /dev/null

if [ $? -eq 0 ]; then
    echo "L'utilisateur existe déjà dans le groupe"
    exit 1
fi

#On ajoute l'utilisateur s'il n'existe pas déjà
sed -i ${line}s/$/,$1/g test.conf

if [$? -eq 1]; then
    echo "Problème lors de l'ajout de l'utilisateur, on revient à la conf précédente !"
    cp -v ~/smb.conf.bak /etc/samba.smb.conf
    exit 1
fi

#On test le fichier de conf
testparm -s /etc/samba/smb.conf
if [ $? -eq 1 ]; then
    echo "Problème lors de l'ajout de l'utilisateur, on revient à la conf précédente !"
    cp -v ~/smb.conf.bak /etc/samba.smb.conf
    exit 1
else
    echo "Utilisateur ajouté correctement !"
fi

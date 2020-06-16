# DigitLBM

LIGGGHTS-PUBLIC est un logiciel open-source du CFDEM utilisable sous la licence GNU Public
Tous les droits et licences sont disponibles sur www.cfdem.com

https://github.com/CFDEMproject/LIGGGHTS-PUBLIC
https://www.cfdem.com/liggghts-open-source-discrete-element-method-particle-simulation-code



----------------------------------------------------------------------------------------------------
Pour installer LIGGGHTS (VERSION A CONFIRMER)

Premiere etape : 
  git clone https://github.com/CFDEMproject/LIGGGHTS-PUBLIC.git

Deuxieme etape selon votre version de ubuntu :
Ubuntu 16.04LTS:
  sudo apt-get install openmpi-bin libopenmpi-dev libvtk6.2 libvtk6-dev
-----
Ubuntu 17.10:
  sudo apt-get install openmpi-bin libopenmpi-dev libvtk6.3 libvtk6-dev
  
Troisieme etape :
  cd /LIGGGHTS-PUBLIC/src/
  
Quatrieme etape :
  make auto
  (d'autres options sont possibles telles que "make serial" ou "make mpi" , examinez la doc 
  pour comprendre leur usage)
  
Etape optionnelle : 
Vous pouvez faire "make yes-all" pour intégrer les differents packages ou
modifier le fichier /LIGGGHTS-PUBLIC/src/MAKE/MAkefile.user pour integrer d'autes packages
Puis refaites "make auto" pour update le programme

PS : vous pouvez creer vos propres fichiers .cpp et .h pour les integrer a LIGGGHTS si l'envie 
vous prends mais pensez à faire make auto.

Cinquieme etape :(testée sur Debian 10)
  sudo ln -s ~/LIGGGHTS-PUBLIC/src/lmp_auto /usr/local/bin/
l'executable etant dans /LIGGGHTS-PUBLIC/src/
faites en un executable (lmp_auto peut etre lmp_mpi oou lmp_serial selon votre commande make precedente)



----------------------------------------------------------------------------------------------------
UTILISATION DE LIGGGHTS
Forme recommandé (selon votre lmp_*)
lmp_auto -in fichier_LIGGGHTS
vous pouvez aussi faire 
lmp_auto < fichier_LIGGGHTS
mais quelques erreurs donc a éviter

les fichiers LIGGGHTS peuvent etre sous n'importe quelle forme. CFDEM recommmande la forme suivante
in.nom_du_programme
Exemple : in.laser_beam
La forme d'ecriture n'a aucune incidence mais c'est preferable
car on pourra avoir different types de fichiers comme les data, restart, log ou script.

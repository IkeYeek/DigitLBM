# DigitLBM
LICENCE
-
LIGGGHTS-PUBLIC est un logiciel open-source du CFDEM utilisable sous la licence GNU Public
Tous les droits et licences sont disponibles sur www.cfdem.com

https://github.com/CFDEMproject/LIGGGHTS-PUBLIC

https://www.cfdem.com/liggghts-open-source-discrete-element-method-particle-simulation-code



----------------------------------------------------------------------------------------------------
INSTALLATION DE LIGGGHTS  (VERSION A CONFIRMER)
-
Pour installer LIGGGHTS suivez ces etapes en cas d'erreur se referer à la documenttion officielle de LIGGGHTS

https://www.cfdem.com/media/DEM/docu/Manual.html

Premiere etape :
-
  <code> git clone https://github.com/CFDEMproject/LIGGGHTS-PUBLIC.git </code>

Deuxieme etape selon votre version de ubuntu :
Ubuntu 16.04LTS:
  <code> sudo apt-get install openmpi-bin libopenmpi-dev libvtk6.2 libvtk6-dev </code>
Ubuntu 17.10:
  <code> sudo apt-get install openmpi-bin libopenmpi-dev libvtk6.3 libvtk6-dev </code>
  
Troisieme etape : 
-
  <code> cd /LIGGGHTS-PUBLIC/src/ </code>
  
Quatrieme etape : 
-
  <code> make auto </code>
  (d'autres options sont possibles telles que "make serial" ou "make mpi" , examinez la doc 
  pour comprendre leur usage)
  
Etape optionnelle : 
-
Vous pouvez faire <code>make yes-all </code> pour intégrer les differents packages ou
modifier le fichier /LIGGGHTS-PUBLIC/src/MAKE/MAkefile.user pour integrer d'autes packages
Puis refaites <code> make auto </code> pour update le programme

PS : vous pouvez creer vos propres fichiers .cpp et .h pour les integrer a LIGGGHTS si l'envie 
vous prends mais pensez à faire make auto.

Cinquieme etape :(testée sur Debian 10)
-
  <code> sudo ln -s ~/LIGGGHTS-PUBLIC/src/lmp_auto /usr/local/bin/ </code>
l'executable etant dans /LIGGGHTS-PUBLIC/src/
faites en un executable (lmp_auto peut etre lmp_mpi oou lmp_serial selon votre commande make precedente)



----------------------------------------------------------------------------------------------------
UTILISATION DE LIGGGHTS
-
Forme recommandé (selon lmp_serial ou lmp_mpi ou lmp_auto)
<code> lmp_auto -in fichier_LIGGGHTS </code>
vous pouvez aussi faire 
<code> lmp_auto < fichier_LIGGGHTS </code>
mais quelques erreurs donc a éviter

les fichiers LIGGGHTS peuvent etre sous n'importe quelle forme. CFDEM recommmande la forme suivante
in.nom_du_programme
Exemple : in.laser_beam
La forme d'ecriture n'a aucune incidence mais c'est preferable
car on pourra avoir different types de fichiers comme les data, restart, log ou script.

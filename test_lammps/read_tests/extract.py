
title = "TEST \n"

source = open("carre.agdd","r")

dest = open("extract.data","w")

nbAtoms = source.readline().rstrip('\n\r')

dest.write(title)

for ligne in source:
    donnees = ligne.rstrip("\n\r").split("\t")
    dest.write("%s \n" % donnees[2])



title = "TEST \n"

source = open("1cm_no_plate.csv","r")

dest = open("extract.data","w")

nbAtoms = source.readline().rstrip('\n\r')

dest.write(title)




for ligne in source:
    donnees = ligne.rstrip("\n\r").split(",")
    dest.write("%s \n" % donnees[1])


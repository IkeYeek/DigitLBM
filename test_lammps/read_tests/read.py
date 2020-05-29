
title = "TEST \n"

source = open("1cm_no_plate.csv","r")

dest = open("output.data","w")

nbAtoms = source.readline().rstrip('\n\r')

dest.write(title)
dest.write("\n")
dest.write("%s atoms \n" % nbAtoms)
dest.write("1 atom types \n")

dest.write("-7e-3 7e-3 xlo xhi\n-2e-5 2e-5 ylo yhi\n-2e-4 2e-4 zlo zhi\n")

dest.write("\n")
dest.write("Atoms\n")
dest.write("\n")

i=1

for ligne in source:
    donnees = ligne.rstrip("\n\r").split(",")
    dest.write("%s %s %s %s %s %s %s\n" % (i, "1",donnees[3],"2700",donnees[0], donnees[2],donnees[1]))
    i=i+1

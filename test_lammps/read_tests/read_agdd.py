from math import *

title = "output_agdd.data"

source = open("carre.agdd","r")

dest = open(title,"w")

nbAtoms = source.readline().rstrip('\n\r')

nbRepY = 1

nbAtoms = str((int(nbAtoms)*nbRepY))

dest.write(title)
dest.write("\n \n")
dest.write("%s atoms \n" % nbAtoms)
dest.write("1 atom types \n")

maxD = 0
minD = 1

maxX = 0
minX = 0

maxY = 0
minY = 0

maxZ = 0
minZ = 0

for ligne in source:
        initData = ligne.rstrip("\n\r").split("\t")
        x = float(initData[0])
        y = float(initData[2])
        z = float(initData[1])
        D = float(initData[4])
        if x > maxX :
            maxX = x
        if y > maxY :
            maxY = y
        if z > maxZ :
            maxZ = z

        if x < minX :
            minX = x
        if y < minY :
            minY = y
        if z < minZ :
            minZ = z

        if D > maxD :
            maxD = D
        if D < minD :
            minD = D

deltaX = maxX+abs(minX)
deltaY = maxY+abs(minY)
deltaZ = maxZ+abs(minZ)
roundMaxD = (ceil((maxD * 1e5)) * 1e-05)

dest.write("0 "+str(deltaX + (2 * roundMaxD))+" xlo xhi\n")
dest.write("0 "+str(deltaY * nbRepY + 2 * roundMaxD)+" ylo yhi\n")
dest.write("0 "+str(deltaZ + (2 * roundMaxD))+" zlo zhi\n")

#dest.write("-7e-3 7e-3 xlo xhi\n-2e-5 2e-5 ylo yhi\n-2e-4 2e-4 zlo zhi\n")

dest.write("\n")
dest.write("Atoms\n")
dest.write("\n")

i=1
for rep in range(nbRepY):
    source.seek(0)
    source.readline()
    #print("CHECK "+str(rep))
    for ligne in source:
        donnees = ligne.rstrip("\n\r").split("\t")
        #x = (float(donnees[0]) + ((rep * deltaX) + roundMaxD + abs(minX)))
        x = (float(donnees[0]) + roundMaxD + abs(minX))
        y = (float(donnees[2]) + ((rep * deltaY) + roundMaxD + abs(minY)))
        #y = (float(donnees[2]) + roundMaxD + abs(minY))
        #z = (float(donnees[1]) + ((rep * deltaZ) + roundMaxD + abs(minZ)))
        z = (float(donnees[1]) + roundMaxD + abs(minZ))
        D = (float(donnees[4])*2)
        #print("CHECk %s %s %s "%(x,y,z))
        dest.write("%s %s %s %s %s %s %s\n" % (i, "1",D,"2700",x,y,z))

        i=i+1

source.close()
dest.close()

verif = open(title,"r")

verif.readline()
verif.readline()
verif.readline()
verif.readline()
verif.readline()
verif.readline()
verif.readline()
verif.readline()
verif.readline()
verif.readline()

verifMinX = 1
verifMaxX = 0

verifMinY = 1
verifMaxY = 0

verifMinZ = 1
verifMaxZ = 0

for ligne in verif:
        data = ligne.rstrip("\n\r").split(" ")
        #print("TEST %s %s %s %s %s" % (data[0],data[1],data[2],data[3],data[4]))
        x = float(data[4])
        y = float(data[5])
        z = float(data[6])

        if x > verifMaxX :
            verifMaxX = x
        if y > verifMaxY :
            verifMaxY = y
        if z > verifMaxZ :
            verifMaxZ = z

        if x < verifMinX :
            verifMinX = x
        if y < verifMinY :
            verifMinY = y
        if z < verifMinZ :
            verifMinZ = z

print("minX = "+str(minX)+" ,minY = "+str(minY)+" ,minZ = "+str(minZ))
print("minX =  "+str(abs(minX))+" ,minY =  "+str(abs(minY))+" ,minZ =  "+str(abs(minZ)))
print("maxX =  "+str(maxX)+" ,maxY =  "+str(maxY)+" ,maxZ =  "+str(maxZ))
print("minD =  "+str(minD)+" ,maxD = "+str(maxD))
print("arrondi maxD "+str(roundMaxD))
print("deltaX = "+str(deltaX))
print("deltaY = "+str(deltaY))
print("deltaZ = "+str(deltaZ))

print("VERIF OUTPUT")
print("verifMinX = "+str(verifMinX)+" ,\tverifMaxX = "+str(verifMaxX))
print("verifMinY = "+str(verifMinY)+" ,\tverifMaxY = "+str(verifMaxY))
print("verifMinZ = "+str(verifMinZ)+" ,\tverifMaxZ = "+str(verifMaxZ))

import re
import os
import numpy as np

#####################################################################
# Write node coordinates into separate files
#####################################################################

inputName = 'jobname'

fin = open(inputName+'.inp', 'r')
fout_main = open(inputName+'-modify.inp', 'w')

nodelistID = ord('A')
nodecoordEnv = False

for line in fin:
    line = line.rstrip('\r\n')
    if nodecoordEnv:
        if not re.match(r'\*',line):
            fout_sub.write(line+'\n')
            continue
        else:
            # Exit node coordinates enviroment
            nodecoordEnv = False
            fout_sub.close()
    if re.match(r'\*[Nn][Oo][Dd][Ee]\s*,',line) or re.match(r'\*[Nn][Oo][Dd][Ee]\s*$',line):
        # Match "*Node" but not "*Node Output"
        # Enter node coordinates enviroment
        nodecoordEnv = True
        fout_sub = open('oldnodelist-%s.inp' %chr(nodelistID), 'w')
        line_modified = line + ', input=newnodelist-%s.inp' %chr(nodelistID)
        print "Found Node Coordinates"
        nodelistID = nodelistID + 1
    else:
        line_modified = line
    fout_main.write(line_modified+'\n')

fin.close()
fout_main.close()

#####################################################################
# Apply transformations on nodes
#####################################################################

oldnodelistName = 'oldnodelist-A'
newnodelistName = 'newnodelist-A'
forigin = open(oldnodelistName+'.inp', 'r')
ftransf = open(newnodelistName+'.inp', 'w')

tol = 1E-6
for line in forigin:
    data = line.split(',')
    id = int(data[0])
    x = float(data[1])
    y = float(data[2])
    z = float(data[3])

    newx = x
    newy = y
    if z<1.0+tol:
        newz = z*100E-3
    elif z<2.0+tol:
        newz = 100E-3+7E-3*(z-1.0)
    elif z<3.0+tol:
        newz = 107E-3+39E-3*(z-2.0)
    elif z<4.0+tol:
        newz = 146E-3+154E-3*(z-3.0)
    ftransf.write("%7d, %18.10e, %18.10e, %18.10e\n" %(id,newx,newy,newz))

forigin.close()
ftransf.close()

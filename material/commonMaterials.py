# -*- coding: UTF-8 -*-
# A tiny database for materials used in MEMS, flexible electronics
# include mechanical, thermal properties

# Abaqus modules import
from abaqus import *
from abaqusConstants import *
from caeModules import *

# Current Model
currentModel = mdb.models.values()[0]

#####################################################################
# Metal and inorganic
#####################################################################

## Gold, Au
currentModel.Material(name='Au')
currentModel.materials['Au'].Elastic(table=((78E3, 0.44), ))
# Source: Zhang et al. Advanced Functional Materials 24.14 (2014): 2028-2037.

## Copper, Cu
currentModel.Material(name='Cu')
currentModel.materials['Cu'].Elastic(table=((119E3, 0.34), ))
# Source: Zhang et al. Advanced Functional Materials 24.14 (2014): 2028-2037.

## Nickel, Ni
currentModel.Material(name='Ni')
currentModel.materials['Ni'].Elastic(table=((200E3, 0.31), ))
# Source: Zhang et al. Advanced Functional Materials 24.14 (2014): 2028-2037.

## Silicon, Si
currentModel.Material(name='Si')
currentModel.materials['Si'].Elastic(table=((130E3, 0.27), ))
# Source: Xu, Sheng, et al. Science 347.6218 (2015): 154-159.

#####################################################################
# Polymer
#####################################################################

## Polyimide, PI
currentModel.Material(name='PI')
currentModel.materials['PI'].Density(table=((1.42E-3, ), ))
# Source: http://www.mit.edu/~6.777/matprops/polyimide.htm
currentModel.materials['PI'].Elastic(table=((2.5E3, 0.34), ))
# Source: http://www.mit.edu/~6.777/matprops/polyimide.htm

## SU-8 Photoresist, SU-8
currentModel.Material(name='SU-8')
currentModel.materials['SU-8'].Density(table=((1.19E-3, ), ))
# Source: http://www.mit.edu/~6.777/matprops/su-8.htm
currentModel.materials['SU-8'].Elastic(table=((4.02E3, 0.22), ))
# Source: http://www.mit.edu/~6.777/matprops/su-8.htm

## PDMS
currentModel.Material(name='PDMS')
# (10:1) Young's Modulus 2.99 MPa
# (20:1) Young's Modulus 841 KPa
# (30:1) Young's Modulus 232 KPa
# (40:1) Young's Modulus 72 KPa
# (50:1) Young's Modulus 23.7 KPa
# Source: Yu et al. Journal of Materials Research 30.18 (2015): 2702-2712.
young = 2.99
poisson = 0.49
Hyper_C10=young/(5*(1.0+poisson))
Hyper_C01=young/(20*(1.0+poisson))
Hyper_D1 =6*(1.0-2*poisson)/young
currentModel.materials['PDMS'].Hyperelastic(materialType=ISOTROPIC,
    testData=OFF, type=MOONEY_RIVLIN, volumetricResponse=VOLUMETRIC_DATA,
    table=(( Hyper_C10, Hyper_C01, Hyper_D1), ))

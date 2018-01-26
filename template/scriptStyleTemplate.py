################################################################################
################################### Imports ####################################
################################################################################

# Abaqus/CAE Import
from abaqus import *
from abaqusConstants import *
from caeModules import *

# Abaqus/Viewer Import
from odbAccess import *
# Backward Compatibility
# import testUtils
# testUtils.setBackwardCompatibility()

# Math Libraries
import math
import numpy as np

# System Libraries
import sys
import os
import time
import csv

################################################################################
############################## Model Parameters  ###############################
################################################################################

# Physical Model Parameters
L_BOX = 1.0
W_BOX = 1.0
H_BOW = 1.0

# FEA Model Parameters
sizeMeshGlobal = L_BOX*0.2
sizeMeshLocalRefine = sizeMeshGlobal*0.5
numMeshThick = 4
tol = sizeMeshLocalRefine*1E-2

# Model Information
modelName = 'testModel'

jobInfo = {}
jobInfo['jobName'] = modelName
jobInfo['jobDescription'] = 'None'
jobInfo['nCPUs'] = 2

################################################################################
############################ Model Initialization  #############################
################################################################################

########## Initialize Database and Model ##########
mdb = Mdb()
currentModel = mdb.Model(name=modelName)

########## Open an existing model ##########

########## Initialize Database and Model ##########

################################################################################
######################### Shared Components Definition #########################
################################################################################

##### Materials

# Material-1
currentModel.Material(name='Material-1')
currentModel.materials['Material-1'].Elastic(table=((100E3, 0.3), ))

##### Sections

##### Profiles

##### Functions


################################################################################
############################### Parts Definition ###############################
################################################################################

########## currentModel.parts['PART-1'] ##########

##### Sketch
s = currentModel.ConstrainedSketch(name='outline_PART-1', sheetSize=10.0)
s.rectangle(point1=(0.0,0.0),point2=(L_BOX,W_BOX))
# s.Line(point1=,point2=)
# s.ArcByCenterEnds(center=,point1=,point2=)
# s.CircleByCenterPerimeter(center=,point1=)

##### Create a part
p = currentModel.Part(name='PART-1',
    dimensionality=THREE_D, type=DEFORMABLE_BODY)
# dimensionality: THREE_D, TWO_D_PLANAR, and AXISYMMETRIC

##### Feature Creation
p.BaseSolidExtrude(sketch=s, depth=H_BOW)
# p.BaseShell(sketch=s)
# p.BaseShellExtrude(sketch=s, depth=H_BOW)

##### Partition

##### Set (Geometry)

##### Section Assignments

##### Mesh

##### Set (Elements/Nodes)

##### Surface

################################################################################
############################# Assembly Definition ##############################
################################################################################

assem = currentModel.rootAssembly
tmpPart = currentModel.parts['PART-1']
tmpIns = assem.Instance(name='INS-1', part=tmpPart, dependent=ON)

##### Sets & Surfaces

##### Constraints


################################################################################
############################## Step Definition #################################
################################################################################

########## currentModel.steps['Step-1'] ##########
currentModel.StaticStep(name='Step-1', previous='Initial')
currentModel.steps['Step-1'].setValues(nlgeom=ON, maxNumInc=1500,
            initialInc=0.01, minInc=1e-8, maxInc=0.05)

##### Boundaries and Loads

##### Output Control

##### Step Control (Advanced Control)


################################################################################
############################### Job Definition #################################
################################################################################

##### Save
mdb.saveAs(modelName+'.cae')

##### Job
currentJob = mdb.Job(name=jobInfo['jobName'], model=modelName)
currentJob.setValues(description=jobInfo['jobDescription'])
currentJob.setValues(numCpus=jobInfo['nCPUs'], numDomains=jobInfo['nCPUs'])
currentJob.setValues(nodalOutputPrecision=FULL)

##### Write Input
currentJob.writeInput(consistencyChecking=OFF)

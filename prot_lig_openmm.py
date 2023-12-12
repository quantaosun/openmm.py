# This script is written by quantaosun@gmail.com or https://github.com/quantaosun/openmm.py for OpenMM simulation,2023.

from simtk.openmm import *
from simtk.openmm.app import *
from simtk.unit import *
from sys import stdout
from openmm.app import PDBFile # for final frame pdb generation

# Input Files

prmtop = AmberPrmtopFile('SYS_gaff2.prmtop')
inpcrd = AmberInpcrdFile('SYS_gaff2.crd')

# System Configuration

nonbondedMethod = PME
nonbondedCutoff = 1.0*nanometers
ewaldErrorTolerance = 0.0005
constraints = HBonds
rigidWater = True
constraintTolerance = 0.000001

# Integration Options

dt = 0.002*picoseconds
temperature = 300*kelvin
friction = 1.0/picosecond
pressure = 1.0*atmospheres
barostatInterval = 25

# Simulation Options

# long simulation (default)
#minimizationSteps = 10000
#productionSteps = 50000000  # 100 ns
#equilibrationSteps = 20000000  # 20 ns
##################################################
# short simulation
minimizationSteps = 100000
productionSteps = 10000000  # 10 ns
equilibrationSteps = 5000000  # 5 ns
##################################################

platform = Platform.getPlatformByName('CUDA')
platformProperties = {'Precision': 'single'}
dcdReporter = DCDReporter('prot_lig_prod.dcd', 10000)

minimizationDataReporter = StateDataReporter('stdout', 100, totalSteps=minimizationSteps,
    step=True, time=True, speed=True, progress=True, remainingTime=True, potentialEnergy=True, temperature=True, separator='\t')

equilibrationDataReporter = StateDataReporter(stdout, 5000, totalSteps=equilibrationSteps,
    step=True, time=True, speed=True, progress=True, remainingTime=True, potentialEnergy=True, temperature=True, separator='\t')
productionReporter = StateDataReporter(stdout, 5000, totalSteps=productionSteps,
    step=True, time=True, speed=True, progress=True, remainingTime=True, temperature=True, separator='\t')

dataReporter = StateDataReporter('prot_lig_prod.log', 1000, totalSteps=productionSteps,
    step=True, time=True, speed=True, progress=True, remainingTime=True, potentialEnergy=True, temperature=True, separator='\t')

# Prepare the Simulation

print('Starting molecular dynamics simulaiton......')

print('############################################################################')

print('##  https://github.com/quantaosun/openmm.py ####') 

print('############################################################################')

print('Initialising molecular dynamics....')

print('############################################################################')

print (' This script should only used in GPU platform, CPU not supported.')

print('############################################################################')


import time
# Sleep for 10 seconds
time.sleep(20)

print('############################################################################')
print('Building system...')
topology = prmtop.topology
positions = inpcrd.positions
system = prmtop.createSystem(nonbondedMethod=nonbondedMethod, nonbondedCutoff=nonbondedCutoff,
    constraints=constraints, rigidWater=rigidWater, ewaldErrorTolerance=ewaldErrorTolerance)
system.addForce(MonteCarloBarostat(pressure, temperature, barostatInterval))
integrator = LangevinIntegrator(temperature, friction, dt)
integrator.setConstraintTolerance(constraintTolerance)
simulation = Simulation(topology, system, integrator, platform, platformProperties)
simulation.context.setPositions(positions)
if inpcrd.boxVectors is not None:
    simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)

#########################################################

content = """
###################################################

If you wish to change the simulation time, please modify
these three parameters inside the .py file

#############################################################
Default setting: 10000 steps of minimisation, followed by 10 ns 
of equilibration, 50 ns of production.
##############################################################
Results include
###############################################################
##########          prot_lig_mini.pdb               ##############
##########          prot_lig_equil.pdb              ##############
##########          prot_lig_prod.pdb               ##############
###########         prot_lig_prod.dcd               ##############

##################################################################


#     #      #     #     ######    #    # #     # 
#     #      ##    #     #         #    #  #   #
#     #      #  #  #     ######    #   #   #  #
#     #      #    ##          #      #      #   
 #####       #     #    #######      #      #

This script was written at The University of New South Wales, Sydney.
"""

print(content)


# Minimize and Equilibrate

print('Performing energy minimization...')
#simulation.minimizeEnergy()
simulation.minimizeEnergy(maxIterations=minimizationSteps)

print('Saving the last minimised frame as PDB file...')

positions = simulation.context.getState(getPositions=True).getPositions()
PDBFile.writeFile(topology, positions, open('prot_lig_mini.pdb', 'w'))

simulation.reporters.clear()

time.sleep(10)
print('##############################################')
print('Starting Equilibrating...')
simulation.context.setVelocitiesToTemperature(temperature)
simulation.reporters.append(equilibrationDataReporter)
simulation.step(equilibrationSteps) 

print('Saving the last equilibrated frame as PDB file...')
positions = simulation.context.getState(getPositions=True).getPositions()
PDBFile.writeFile(topology, positions, open('prot_lig_equil.pdb', 'w'))

simulation.reporters.clear()
time.sleep(10)

# Production Simulate
print('##############################################')
print('Production Simulating...')
simulation.reporters.append(productionReporter) # on screen display.
simulation.reporters.append(dcdReporter)
simulation.reporters.append(dataReporter)
simulation.currentStep = 0
simulation.step(productionSteps)
print('##############################################')
# Write the last frame as a PDB file
print('Saving the last frame as PDB file...')

positions = simulation.context.getState(getPositions=True).getPositions()
PDBFile.writeFile(topology, positions, open('prod_lig_prod.pdb', 'w'))
time.sleep(5)
print('Congratulations, your simulation has finished!')


## Background

https://github.com/pablo-arantes has developed an excellent Colab workflow to run the simulation. However, Google Colab sometimes has connection issues or you have to subscribe to get access to a decent GPU, or in some areas, it is just not accessible to connect to Colab easily.

This repo is designed for people who want to do a general molecular dynamic simulation locally using OpenMM with Amber inputs, with much more stability.


## Pre-requirement

OpenMM need to be installed on a Linux platform

## Steps

1.  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/quantaosun/webdock/HEAD?labpath=webdock_v.0.0.2.ipynb) generate ```receptor.pdb``` and ```Docked1.pdb```, or with  Schrodinger/Maestro, or Autodock vina, or any other docking software you could have access to. Alternatively, you can always to install webdock (https://github.com/quantaosun/webdock) into your local Linux, then generate the docked results.

2. [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/quantaosun/pl3_gmx_mmpbsa/HEAD), click to wait loading finished. Alternatively, you can install this repo comes with ambertools (https://github.com/quantaosun/pl3_gmx_mmpbsa)  into your local Linux, then generate the md inputs files as described in step 3.
3. Upload the 2 files from step1,  to generate ```SYS_gaff2.prmtop``` and ```SYS_gaff2.crd```, note, the binder link is not guaranteed if there is high visit volume, if not accessible you can use https://github.com/pablo-arantes/making-it-rain
5. Download this repo to a local Linux with OpenMM installed (If you haven't got one, you could create one by the environment file attached in this repo), and copy the two files in step2, to the same folder as the Python script provided in this repo.

### Inputs 
```
prot_lig_openmm.py
SYS_gaff2.crd
SYS_gaff2.prmtop

```
### Execute the simulation

```python prot_lig_openmm.py ```
It will do a 10 ns equilibration and 50 ns of production by default. You must change the ```prot_lig_openmm.py``` if you want a longer or shorter simulation.


### Output

```
prod_lig_1.pdb
prot_lig_prod.dcd
prot_lig_prod.log
stdout  
```
```prod_lig_1.pdb``` is the final simulated structure, ```prot_lig_prod.dcd``` is the trajectory file.

### Visualisation

In Pymol, load ```prod_lig_1.pdb``` and ```prot_lig_prod.dcd```

![image](https://github.com/quantaosun/general-openmm/assets/75652473/023217fb-4cd5-4751-9fcc-1437588179ac)

## Performance

RTX4090: to simulate 100 nanoseconds for a typical kinase size protein-ligand complex

```
#"Progress (%)"	"Step"	"Time (ps)"	"Potential Energy (kJ/mole)"	"Temperature (K)"	"Speed (ns/day)"	"Time Remaining"
0.0%	1000	8002.000000712723	-768173.560093076	300.0716998151275	0	--
0.0%	2000	8004.00000071313	-767249.5673865234	300.76147916830683	486	    59:13
0.0%	3000	8006.000000713538	-767389.9470499307	301.14007459911784	486	    59:13
0.0%	4000	8008.000000713945	-768387.7632756401	298.08645047906015	486	    59:14
```
## Simulation time
I provided three potential lengths of simulation, you can open ```prot_lig_openmm.py``` to comment or uncomment lines to choose one of the
```
long, 20 ns equilibration + 100 ns production
medium, 10 ns equilibration + 50 ns production
short, 2 ns equilibration + 10 ns production
```
simulations. Like in the section below, I chose the short one by uncommenting those lines.
```
# Simulation Options

# long simulation (default)
#minimizationSteps = 10000
#productionSteps = 50000000  # 100 ns
#equilibrationSteps = 20000000  # 20 ns
###################################################
# medium simulation
#minimizationSteps = 10000
#productionSteps = 25000000  # 50 ns
#equilibrationSteps = 10000000  # 10 ns
###################################################
# short simulation
minimizationSteps = 10000
productionSteps = 10000000  # 10 ns
equilibrationSteps = 4000000  # 2 ns
##################################################
```

## Analysis

```
>>> import mdtraj
>>> from __future__ import print_function
>>> import mdtraj as md
>>> crystal_fn = 'data/native.pdb'
>>> crystal_fn = './prod_lig_1.pdb'
>>> trajectory_fn = './prot_lig_prod.dcd'
>>> crystal = md.load(crystal_fn)
>>> trajectory = md.load(trajectory_fn, top=crystal)
>>> trajectory
<mdtraj.Trajectory with 25 frames, 56495 atoms, 17382 residues, and unitcells at 0x7fdb3bc91c10>
>>> rmsds_to_crystal = md.rmsd(trajectory, crystal, 0)
>>> heavy_atoms = [atom.index for atom in crystal.topology.atoms if atom.element.symbol != 'H']
>>> heavy_rmds_to_crystal = md.rmsd(trajectory, crystal, 0, atom_indices=heavy_atoms)
>>> from matplotlib import pyplot as plt
>>> plt.plot(trajectory.time, rmsds_to_crystal, 'r', label='all atom')
[<matplotlib.lines.Line2D object at 0x7fdaf4842f10>]
>>> plt.plot(trajectory.time, heavy_rmds_to_crystal, 'b', label='heavy atom')
[<matplotlib.lines.Line2D object at 0x7fdaf485c1f0>]
>>> plt.legend()
<matplotlib.legend.Legend object at 0x7fdaf48a94c0>
>>> plt.title('RMSDs to crystal')
Text(0.5, 1.0, 'RMSDs to crystal')
>>> plt.xlabel('simulation time (ps)')
Text(0.5, 0, 'simulation time (ps)')
>>> plt.ylabel('RMSD (nm)')
Text(0, 0.5, 'RMSD (nm)')
```

## Reference
1. https://openmm.org/documentation
2. https://github.com/pablo-arantes


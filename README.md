# General-OpenMM

## Background

https://github.com/pablo-arantes has developed an excellent Colab workflow to run the simulation. This repo is designed for people who want to do a general molecular dynamic simulation locally using OpenMM with Amber inputs. 

With a GPU like RTX4090, the speed can easily achieve around 300 ns/day for a typical kinase protein-small molecule complex.

![image](https://github.com/quantaosun/cheat_MD/assets/75652473/0bb7c2b4-4eee-4c93-905b-1dd0d55c3243)

## Pre-requirement

OpenMM need to be installed in a Linux platform

## Steps

1. https://colab.research.google.com/github/pablo-arantes/Cloud-Bind/blob/main/GNINA.ipynb#scrollTo=wyzlRC-sBY3J to generate receptor.pdb and Docked1.pdb
2. https://github.com/pablo-arantes/making-it-rain to generate SYS_gaff2.prmtop and SYS_gaff2.crd
3. Download this repo to a local Linux with OpenMM installed, and provide the two files in step2, and run ```python prot_lig_openmm.py ```, it will do a 10 ns equilibration and 50 ns of production

### Inputs 
```
prot_lig_openmm.py
SYS_gaff2.crd
SYS_gaff2.prmtop

```
### Execute the simulation

```python prot_lig_openmm.py ```

### Output

```
prod_lig_1.pdb
prot_lig_prod.dcd
prot_lig_prod.log
stdout  
```
```prod_lig_1.pdb``` is the final simulated structure, ```prot_lig_prod.dcd``` is the trajectory file.
## Performance

RTX4090: to simulate 100 nano second for a typical kinase size protein-ligand complex

```
#"Progress (%)"	"Step"	"Time (ps)"	"Potential Energy (kJ/mole)"	"Temperature (K)"	"Speed (ns/day)"	"Time Remaining"
0.0%	1000	8002.000000712723	-768173.560093076	300.0716998151275	0	--
0.0%	2000	8004.00000071313	-767249.5673865234	300.76147916830683	486	    59:13
0.0%	3000	8006.000000713538	-767389.9470499307	301.14007459911784	486	    59:13
0.0%	4000	8008.000000713945	-768387.7632756401	298.08645047906015	486	    59:14
```




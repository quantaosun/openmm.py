## Analysis

- Pymol visualisation, load SYS.pdb, load prot_lig_prod.dcd

### The recommended analysis tool is Bio3D


http://thegrantlab.org/bio3d/articles/online/traj_vignette/Bio3D_md.html 

- R is free on any Unix-like terminal, you can install it easily.

```
sudo apt-get install r-base
```
- Then, install Bio3D within R
```
install.packages("bio3d", dependencies=TRUE)
 ```

RMSD

![image](https://github.com/quantaosun/openmm.py/assets/75652473/427b9b84-6aeb-498f-95fd-cfd9c94bcfd6)

RMSF

![image](https://github.com/quantaosun/openmm.py/assets/75652473/3bd0fb23-00d2-4c07-8d99-f4a3915007ef)

PCA

![image](https://github.com/quantaosun/openmm.py/assets/75652473/2c6afcd3-698c-4894-9a3c-3cd99fb9a391)

PC1 and PC2(blue), residue-wise distribution

![image](https://github.com/quantaosun/openmm.py/assets/75652473/d9a98098-e48c-438a-88b2-93d1da269bea)

Cross-correlation

![image](https://github.com/quantaosun/openmm.py/assets/75652473/80279b61-8ac3-4768-b9b6-8da847247960)


### Alternatively


Note this analysis RMSD plot is an image plot or reversed plot of a normal RMSD since it 
utilised the last PDB as a reference instead of the initial one. It doesn't matter in a sense as long as you can observe that the curve has already reached the flat status.

<img width="681" alt="image" src="https://github.com/quantaosun/openmm.py/assets/75652473/8f82d4c7-98ab-41de-8736-d2f41056ef77">

![image](https://github.com/quantaosun/openmm.py/assets/75652473/2ac4bdd0-615a-45e4-b917-5085fa2a08d4)



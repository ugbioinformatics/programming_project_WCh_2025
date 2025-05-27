import subprocess
import re
import os
import operator
import xyz2mol
import read_xtbout_file as xtb
import read_mopac_file as mopac
from rdkit import Chem

def shell(cmd, shell=False):

    if shell:
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        cmd = cmd.split()
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, err = p.communicate()
    return output


def rank_by_energy(e_cut,base_name,entropy_correction,method):
# The code will find all compounds with an energy less than the reactant plus all compounds with
# an a higher energy but within "e_cut" kcal/mol. The molecules will be ranked with the lowest 
# energy compound first
    energy_ranked_molecules = []
    au_to_kcal = 627.51

# File extention for GFN-xTB or MOPAC output files. Change if using something else
    if method == "xtb":
        file_names =  shell('ls *.xtbout', shell=True).split("\n")[:-1]
    if method == "mopac":
#        print( shell('ls *.out', shell=True).decode('utf-8').split("\n")[:-1])
        file_names =  shell('ls *.out', shell=True).decode('utf-8').split("\n")[:-1]
        print(file_names)
    
    fragment_energies = {}
    for file_name in file_names:
# Assumes GFN-xTB or MOPAC output files. You need to write your own parser if you use another program
        if method == "xtb":
            energy = xtb.get_energy(file_name)
        if method == "mopac":
            energy = mopac.get_energy(file_name)
        energy += entropy_correction
        fragment = file_name.split("+")[0]
        if fragment not in fragment_energies:
            fragment_energies[fragment] = [energy,file_name]
        elif energy < fragment_energies[fragment][0]:
            fragment_energies[fragment] = [energy,file_name]
    
    energies = {}
    for fragment in fragment_energies:
        name = fragment[:-1]
        energy = fragment_energies[fragment][0]
        file_name = fragment_energies[fragment][1]
        if name not in energies:
            energies[name] = [energy,file_name]
        else:
            energies[name][0] += energy
            energies[name][1] += ","+ file_name

# The compund(s) labelled xxx0A,B, etc is assumed to be the starting structure used to create
# the elementary steps, i.e. the reactant.
    for name in energies:
       if name.split(base_name)[1][:1] == "0":
           reactant_energy = energies[name][0]
    
# The code will find all compounds with an energy less than the reactant plus all compounds with
# an a higher energy but within "e_cut" kcal/mol. The molecules will be ranked with the lowest 
# energy compound first
    sorted_energies = sorted(energies.items(), key=operator.itemgetter(1))
#    min_energy = sorted_energies[0][1][0]
    for name, (energy,file_name) in sorted_energies:
        e_diff = (energy - reactant_energy)*au_to_kcal
        if e_diff < e_cut:
#           print name, e_diff, file_name
            energy_ranked_molecules.append((name,round(e_diff,1),file_name))

    return energy_ranked_molecules

def files2mol(energy_ranked_files,charged_fragments,method):
# the code assumes GFN-xTB or mopac output files. If you want to use another program add another parser
    smiles_list = []
    molecules = []
    for name,energy, file_name in energy_ranked_files:
        fragment_smiles_list = []
        for fragment_file in file_name.split(","):
            try:
                if method == "xtb":
                    charge,atomicNumList,xyz_coordinates = xtb.read_xtbout_file(fragment_file)
                if method == "mopac":
                    charge,atomicNumList,xyz_coordinates = mopac.read_mopac_file(fragment_file)
                    print(fragment_file)
#                    print(charge,atomicNumList,xyz_coordinates)
            except:
                print(fragment_file)
            fragment_mol = xyz2mol.xyz2mol(atomicNumList,charge,xyz_coordinates,charged_fragments)
            fragment_smiles = Chem.MolToSmiles(fragment_mol)
            fragment_smiles_list.append(fragment_smiles)
        smiles = ".".join(fragment_smiles_list)
        if smiles not in smiles_list:
            molecules.append((name, smiles, energy, file_name))
            smiles_list.append(smiles)

    return molecules

        
if __name__ == "__main__":
# The compund(s) labelled xxx0A,B, etc is assumed to be the starting structure used to create
# the elementary steps, i.e. the reactant.
# A, B, etc refer to fragments and the energies are combined. Example: the reactant is 
# CH4 + H2O, so xxx0A and xxx0B refer to CH4 and H2O, respectively and the energy of xxx0
# is the sum of these two energies.
# The code will find all compounds with an energy less than the reactant plus all compounds with
# an a higher energy but within "e_cut" kcal/mol. The molecules will be ranked with the lowest 
# energy compound first
    e_cut = 20. #kcal/mol

# Rough estimate of the translational entropy correction -TS at 298K which is added to the energy.
# This is important when comparing the energy of one molecule to that of two, e.g. CH3OH vs CH3O + H
# If you are using free energies to rank your compounds this should be set to 0.
    au_to_kcal = 627.51
    entropy_correction = -10./au_to_kcal

# Make charged fragments, e.g. CH3O- + H+ instead of CH3O + H
    charged_fragments = False

# It is assumed that the directory name and file names are same, e.g. directory0A for the reactant
    directory = "formic_acid"
    #directory = "ROOR"
    
    os.chdir(directory)

# pick the method you want to use. The choices are currently GFN-xTB and MOPAC
    #method = "xtb"
    method = "mopac"

    energy_ranked_files = rank_by_energy(e_cut,directory,entropy_correction,method)
    energy_ranked_molecules = files2mol(energy_ranked_files,charged_fragments,method)

    for name, smiles, energy, file_name in energy_ranked_molecules:
        print(name, smiles, energy, file_name)

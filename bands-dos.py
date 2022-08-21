#!/usr/bin/env python3
# ------------------------------------------------------------------
# [Author] Yue-Wen Fang [Email] fyuewen@gmail.com
#          Description
#   [usage] python pbands-dos.py
# [Purpose] Plot the phonon dispersions and DOS from phonon calculations
#          History
#  HISTORY
# Version-ID; Time; Reason
# Version 0.1.0; 2022/08/16; Script creation for plotting phonon bands and DOS (also projected DOS)
# ------------------------------------------------------------------

import yaml
import pandas as pd
import numpy as np
from pymatgen.io.vasp.inputs import Poscar

import matplotlib.style
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use('classic')
mpl.rcParams['figure.facecolor'] = '1'
#if choose the grey backgroud, use 0.75
# mpl.rcParams['figure.figsize'] = [12,6]
mpl.rcParams['lines.linewidth'] = 3.5
mpl.rcParams["axes.linewidth"]  = 3.5 #2. #change the boarder width
mpl.rcParams['legend.fancybox'] = True
mpl.rcParams['legend.framealpha'] = 0.8
mpl.rcParams['legend.fontsize'] = 32
mpl.rcParams['legend.title_fontsize'] = 32


mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'Arial'
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.rm'] = 'sans'
mpl.rcParams['mathtext.it'] = 'sans:italic'
mpl.rcParams['mathtext.default'] = 'it'

mpl.rcParams['legend.scatterpoints'] = 1 #scatterpoints,
#it's the numer of maker points in the legend when
#creating a legend entry for a scatter plot
mpl.rcParams["axes.formatter.useoffset"]=False #turn off the axis offset-values.
# If on. the axis label will use a offset value by the side of axis
#mpl.rcParams["axes.linewidth"]  = 2.0 #change the boarder width
#plt.rcParams["axes.edgecolor"] = "0.15" #change the boarder color
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from matplotlib.gridspec import GridSpec
plt.style.use("seaborn-paper")

ticklabel_size = 22
mpl.rcParams['xtick.labelsize'] = ticklabel_size
mpl.rcParams['ytick.labelsize'] = ticklabel_size

fig = plt.figure()
gs = GridSpec(1, 4, wspace=0)
ax1 = fig.add_subplot(gs[:,:-1])
ax2 = fig.add_subplot(gs[:,-1])
# create an figure object
# fig = plt.figure()
# ax = fig.add_subplot(111)

# read band.yaml file and plot distance as a function of frequency
with open('sumo_band.yaml', 'r') as stream:
    data_loaded = yaml.load(stream, Loader=yaml.FullLoader)
    print(type(data_loaded))
    # print the keys in the dictionary data_loaded
    print(data_loaded.keys())
    print(type(data_loaded['phonon']))
    print(data_loaded['phonon'][0].keys())
    distance = data_loaded['phonon'][0]['distance']
    print(data_loaded['phonon'][0]['distance'])
    branches = len(data_loaded['phonon'][0]['band'])

    # create an empty dataframe
    column_list = []
    for i in range(branches):
        column_list.append('band'+str(i+1))
    column_list.insert(0, 'distance')
    print(column_list)
    df = pd.DataFrame(columns=column_list) # Note that there are now row data inserted.
    # print(df)
    bands_data=[]
    for i in data_loaded['phonon']:
        band_for_each_branch = []
        # print(i)
        # input('input')
        distance = i['distance']
        for j in i['band']:
            k = list(map(float, j.values()))
            band_for_each_branch.append(k[0])
        band_for_each_branch.insert(0, i['distance'])
        bands_data.append(band_for_each_branch)
        # df = pd.DataFrame([band_for_each_branch], columns=column_list)
    print(bands_data)
    print(len(bands_data))
    df = pd.DataFrame(bands_data, columns=column_list)
    print(df.head(10))
    print(df.shape)
    print(df.columns)

    dists = []
    dists.append([i['distance'] for i in data_loaded['phonon']])
    print('dists is', dists)

    l = []
    p = []
    try:
        for i in data_loaded['phonon']:
            if 'label' in i:
                l.append(i['label'])
            if len(l) == 0:
                raise Exception
    except:
        for i, j in data_loaded['labels']:
            l.append(i)
            if len(l) == len(data_loaded['labels']):
                l.append(j)

    # replace any element including 'G' in l using '$\Gamma$' if it is in l
    # for i in range(len(l)):
    #     print(i)
    # l_tex = ["$" + i + "$" for i in l]
    l_tex = l
    for i in range(len(l_tex)):
        if 'G' in l_tex[i]:
            l_tex[i] = '$\mathrm{\Gamma}$'
    print('l is', l_tex)
    # input('input:')

    step = []
    segments = data_loaded['segment_nqpoint']
    sum_step = 0
    for i in segments:
        sum_step = sum_step + i
        step.append(sum_step)
    #insert 0 to step as the first element of the list
    print('step is', step)
    # input('input: ')
    # extract the distance in df['distance'] according to rcol[step]
    # get three values in df['distance']
    # rcol = df['distance'].values.tolist()
    high_symmetry_distance = []
    # get the row values in df['distance'] using values in step as the index
    for i in step:
        high_symmetry_distance.append(df['distance'].values[i-1])
    high_symmetry_distance.insert(0, 0)
    print('high_symmetry_distance is', high_symmetry_distance)
    print('high_symmetry_distance is', high_symmetry_distance)

df.plot(x='distance', color='orange',ax=ax1, legend=False)
    # ax.plot(df['distance'], df['band1'], color='blue', label='band1')
ax1.set_ylim([-2,80])
ax1.set_xlim([0,df['distance'].max()])
print(df['distance'].max())
# add a horizontal line at y=0
ax1.axhline(y=0, color='black', linestyle='--', linewidth=1.5)
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1.5)


ax1.set_xticks(high_symmetry_distance)
ax1.set_xticklabels(l_tex)
# hide xlabel for ax1
ax1.set_xlabel('')



########################plot the figure in ax2##############################
### you should have 'projected_dos.dat' and 'POSCAR' in the same directory as this script
# try to read POSCAR other raise the erorr of file not found
try:
    struct = Poscar.from_file('POSCAR')
    print(struct)
    elements = struct.site_symbols
    print('elements is ', elements)
    # get the number of atoms for Be, Ba, and H
    natoms = struct.natoms
    print('natoms is', natoms)
    # create a list in the range of 1 to 20

    # create a list with element combining the element in elemetns and natoms
    # element_list = [i for i in range(1, 21)]
    col_list = []
    for i in range(len(elements)):
        for j in range(natoms[i]):
            col_list.append(str(elements[i])+str(j+1))
    print('col_list is', col_list)

    # for i in elements:
    #     # sum_atom = 0
    #     for j in range(0,len(elements)):
    #         for k in natoms[j]:
    #             for m in range(0, k):
    #                 column_list.append(str(i)+'_'+str(m))
    # print('column_list is', column_list)
    #
    # num_of_Be = elements.count('Be')
    # num_of_Ba = elements.count('Ba')
    # num_of_H = elements.count('H')
    # total_atoms = num_of_Be + num_of_Ba + num_of_H
    # number of atoms for each element in POSCAR
    # input('input')
except:
    print('POSCAR not found')
    raise Exception

try:
    # insert 'thz' to  col_list
    col_list.insert(0, 'thz')
    dos = pd.read_csv('projected_dos.dat', sep='\s+', header=None, skiprows=[0], names=col_list)
    print(dos.head(10))
    # sum up the columns including the keyword 'H' in column name
    for i in elements:
        print(i)
        # sum the dos column including the keyword i in column name and save it in a new column in dos
        list = dos.columns[dos.columns.str.contains(i)]
        print('list is', list)
        # input('intpu')

        dos[i] = dos[dos.columns[dos.columns.str.contains(i)]].sum(axis=1)
        # print('dos[i]', dos[i])
        ax2.plot(dos[i], dos['thz'], label = i)
        ax2.set_ylim([-2,80])
        # remove the xticklabels for ax2
        ax2.set_xticklabels([])
        ax2.set_yticklabels([])
        ax2.set_xlabel('DOS', fontsize=22, labelpad=5)
        # ax2.legend(loc='upper right')
        # sum_i = dos[dos.columns.str.contains(i)].sum(axis=1)
        # print(len(sum_i))
        # print(sum_i.shape)
        # print(sum_i)
    # input('input')

    # sum_Ba = dos[dos['element'] == i].sum(axis=1)


except:
    print('projected_dos.dat not found')
    raise Exception
plt.legend(fontsize=22)

ax1.tick_params(direction='in', length=8, width=3, colors='k',
                grid_color='grey', grid_alpha=0.7, top=True, right=False)
ax2.tick_params(direction='in', length=8, width=3, colors='k',
                grid_color='grey', grid_alpha=0.7, top=True, right=False)
fig.set_size_inches(12,6)
plt.tight_layout()
plt.show()
# save the figure as a pdf file
# fig.savefig('ph-bands-dos.pdf')
from matplotlib.backends.backend_pdf import PdfPages
pp1 = PdfPages('./BeBaH4-100GPa-phbands.pdf')
pp1.savefig(fig)
pp1.close()

######################example segment for debug and test #############################
    # df.plot(x='distance', y=column_list, kind='line')
    # plt.show()

    # band_for_each_breanch = []
    # for j in data_loaded['phonon'][0]['band']:
    #     # print(j.values())
    #     # convert the dict_values to float
    #     k = list(map(float, j.values()))
    #     # print(k[0])
    #     band_for_each_breanch.append(k[0])
    # band_for_each_breanch.insert(0, distance) # insert the distance to the first element of the list
    # print(band_for_each_breanch)
    # # create a column list for the band_for_each_breanch including
    # # ['distance', 'band1', 'band2', 'band3', 'band4', 'band5'..'band60']
    # df = pd.DataFrame([band_for_each_breanch], columns=column_list)
    # print(df)
##########################################################################################

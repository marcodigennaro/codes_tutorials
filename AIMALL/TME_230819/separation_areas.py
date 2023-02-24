#!/home/mdi0316/anaconda2/bin/python
import numpy as np
import os
import commands
import re
import pandas as pd


def format_table_into_file(headers, values, file_):
    """The file is an open file object at the correct location
        headers is a list of column headers
        values is a dictionary with a list of values on all header keys,
        the lists inside the values, must have the same length
    """
    table_row_length = len(values[headers[0]])
    lpads_per_key = dict()
    for key in headers:
        lpads_per_key[key] = len(key)
        if len(values[key]) != table_row_length:
            raise ValueError("Values on the key:%s have a length:%s instead of:%s" % (key, len(values[key]), table_row_length))
        for value in values[key]:
            if len(str(value)) > lpads_per_key[key]:
                lpads_per_key[key] = len(str(value))

    for key in headers:
        file_.write(key.ljust(lpads_per_key[key] + 4))

    file_.write('\n')

    for i in range(table_row_length):
        for key in headers:
            file_.write(str(values[key][i]).ljust(lpads_per_key[key] + 4))
        file_.write('\n')


def parse_index_out_of_filename(infile):
    rex = re.compile("([0-9]+)")
    match = rex.match(infile)
    if match:
        return ''.join(match.groups())


def get_infiles_in_order(input_path=None, reverse=False):
    """ Works for files which have a number at the end of the filename."""
    list_of_files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
    list_of_ordered_files = sorted(list_of_files, key=lambda x: int(os.path.splitext(x)[0]), reverse=reverse)
    return list_of_ordered_files


def get_area_IAS_from_sumfile(inpath=None, sumfile=None, outpath=None):
    missing_data = []
    atom_noinfo = []
    header = "Atom,A    Atom,B     Area_IAS(A|B),0.0004     Area_IAS(A|B),0.001     Area_IAS(A|B),0.002"
    get_area = commands.getoutput("awk '/Areas of Interatomic Surfaces/,/Some Properties/' %s" % (inpath + sumfile)).split('\n')
    data_ias = get_area[9:]
    index = parse_index_out_of_filename(sumfile)
    output = '%s%s.dat' % (outpath, index)
    with open(output, 'w') as fa:
        for row in data_ias:
            if 'Data not available' in row:
                missing_data.append(index)
                atom_noinfo.append(row.split()[0])
            output_conditions = [row != ' ', 'Some' not in row, 'Total' not in row, 'Data' not in row, '-' not in row]
            if all(output_conditions):
                if 'Atom A' in row:
                    fa.write(header + '\n')
                else:
                    fa.write(row + '\n')
    return index, missing_data, atom_noinfo


def read_table_from_file(file_, dtype=None):
    """Reads in a txt/dat file, ordered in culomns given by the header. Returns the content of the
    columns in a dictionary, where the keys are the column names. """
    headers = file_.readline().split()
    if dtype is None:
        dtype_formats = [np.dtype('Float64') for key in headers]
        dtype = {'names': tuple(headers),
                 'formats': dtype_formats}
    else:
        dtype = {'names': tuple(headers),
                 'formats': dtype}
    data = np.loadtxt(file_, dtype=dtype)
    return {key: data[key] for key in headers}


def get_separation_area_ions_for_file(file_, anion_atoms=None):
    """input a file object and the list containing the anion atoms e.g. EMIM-BF4: ['B20', 'F21', 'F22', 'F23', 'F24']"""
    data = read_table_from_file(file_, dtype=('|S15', '|S15', np.float, np.float, np.float))
    atom_A = data['Atom,A']
    atom_B = data['Atom,B']
    separea_AB = data['Area_IAS(A|B),0.0004']
    # match contacting atoms
    separea_ions = dict()
    for i in range(len(atom_A)):
        a = str(atom_A[i])
        b = str(atom_B[i])
        if (a not in anion_atoms and b not in anion_atoms):
            continue
        elif (a not in anion_atoms and b in anion_atoms):
            pair = '%s-%s' % (a, b)
            pair_ = '%s-%s' % (b, a)
            if (pair not in separea_ions.keys() and pair_ not in separea_ions.keys()):
                separea_ions[pair] = separea_AB[i]
        elif (a in anion_atoms and b not in anion_atoms):
            pair = '%s-%s' % (a, b)
            pair_ = '%s-%s' % (b, a)
            if (pair not in separea_ions.keys() and pair_ not in separea_ions.keys()):
                separea_ions[pair] = separea_AB[i]
        elif (a in anion_atoms and b in anion_atoms):
            continue
        elif (a not in anion_atoms and b not in anion_atoms):
            raise IOError("The anion atoms given in the input are not present in the file")
    print separea_ions.keys(), sum(separea_ions.values())
    return separea_ions


def match_index_with_distance(input_data=None, column=None, sumfile_indexes=None):
    CM_dist_aim = np.array(sumfile_indexes)
    CM_dist = np.array(list(input_data['CM distance']))
    out_dist = input_data[column]
    search_index = []
    for d in CM_dist_aim:
        print d
        index = list(np.where(CM_dist == d)[0])[0]
        search_index.append(index)
        #print search_index
    aim_dist = [out_dist[i] for i in search_index]
    print 'AIM data found in total: %s \n for ion-distances  at:\n %s A' % (len(aim_dist), aim_dist)
    return aim_dist


BOHR2_ANGSTROM2 = 0.529177**2

ION_SYSTEM = ['EMIM-BF4']
BASIS = ['N311']  # , 'APCseg-1', 'STO']
FUNCTIONALS = ['B3LYP']  # , 'M11', 'PBE0', 'wB97x-D']  # , 'M06', 'TPSS']
theta = [90]
phi = [90]
radius = sorted([2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 3.7, 3.8, 3.9, 4.0, 4.1, 4.3, 4.5, 4.7, 4.9, 5.5, 6.5, 7.5,
                 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.75, 3.85, 3.95, 4.05, 4.2, 4.4, 4.6, 4.8, 5.0, 6.0, 7.0])

DFT_PATH = []
DFT_COLUMN = ['d_ions']

ANION_ATOMS = [['B20', 'F21', 'F22', 'F23', 'F24'], ['P20', 'F21', 'F22', 'F23', 'F24', 'F25', 'F26']]

bindex = 0
findex = 0

for i in range(len(ION_SYSTEM)):
    print 'Ionic system: %s\n' % (ION_SYSTEM[i])
    CONFIG = '%s%s/' % (theta[0], phi[0])
    DATAPATH = 'data/%s/configurations/%s/bader/%s/%s/separeas/' % (ION_SYSTEM[i], CONFIG, BASIS[bindex], FUNCTIONALS[findex])
    if not os.path.exists(DATAPATH):
        os.makedirs(DATAPATH)
    OUTPATH = 'output/descriptors/bader/%s/%s/%s/%s/' % (CONFIG, ION_SYSTEM[i], BASIS[bindex], FUNCTIONALS[findex])
    if not os.path.exists(OUTPATH):
        os.makedirs(OUTPATH)
    SUMFILE_PATH = 'data/%s/configurations/%s/bader/%s/%s/' % (ION_SYSTEM[i], CONFIG, BASIS[bindex], FUNCTIONALS[findex])
    sumfiles = get_infiles_in_order(input_path=SUMFILE_PATH, reverse=False)
    #sumfiles = ['400.sum']
    file_index = []
    missing_data = []
    nodata_dist = []
    for sf in sumfiles:
        ind, ex, at = get_area_IAS_from_sumfile(SUMFILE_PATH, sf, outpath=DATAPATH)
        file_index.append(ind)
        if ex != []:
            noinfo = (ex[0], at)
            nodata_dist.append(ex[0])
            missing_data.append(noinfo)
            print 'Missing data found in the following files, for the atoms: %s, %s\n' % noinfo
    missing_data_dict = {'d_ions': [int(d) / 100. for d in nodata_dist]}
    with open(OUTPATH + 'missing_data.dat', 'w') as m:
            format_table_into_file(['d_ions'], missing_data_dict, m)
    print 'Area_IAS from .sum files written to the following data files:%s' % (file_index)
    print 'Calculates separation between the anion and cation'
    my_files = get_infiles_in_order(input_path=DATAPATH, reverse=False)
    #my_files = ['400.dat']
    d_CM = []
    separation_area_between_atoms = []
    separation_area_between_ions = []
    for my_file in my_files:
        with open(DATAPATH + my_file, 'r') as f:
            index = parse_index_out_of_filename(my_file)
            print my_file, index
            dist = int(index) / 100.
            d_CM.append(dist)
            separation_area_between_atoms.append(get_separation_area_ions_for_file(f, anion_atoms=ANION_ATOMS[i]))
    for data in separation_area_between_atoms:
        separation_area_between_ions.append(sum(data.values()))
    print 'Separation areas: %s' % separation_area_between_ions
    # loads ionic system DataFrame for constant (theta, phi, d_ions) calculation
    # system_da_scan = pd.read_csv(DFT_PATH[i])
    data_dict = {'d_CM': None, 'd_ions': None, 'il_separation_area': None}
    data_dict['d_CM'] = d_CM
    data_dict['d_ions'] = d_CM  # match_index_with_distance(input_data=system_da_scan, column=DFT_COLUMN[i], sumfile_indexes=d_CM)
    data_dict['il_separation_area'] = np.array(separation_area_between_ions) * BOHR2_ANGSTROM2
    column_names = ['d_CM', 'd_ions', 'il_separation_area']
    with open(OUTPATH + 'separation_area.dat', 'w') as f:
            format_table_into_file(column_names, data_dict, f)


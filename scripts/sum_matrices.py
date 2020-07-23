#!/tools/python/3.7.4/bin/python

"""This python script allow to run an hicexplorer pipeline to sum matrices and to do
a diagnostic plot. To run it, you need to give as argument the path of hic_directory
where the script will save the data.

i.e. init_hicexplorer hic_studies/"""

import os, sys
import re


def set_trio(path):
    list = []
    for dir in os.listdir(path):
        if dir.startswith('trio'):
            list.append(dir)
        else:
            continue
    list.sort()
    return list


def write_metadata(trio):
    fh = open(hic_dir + "/metadata.tsv", 'w')
    fh.write("indiv \t protocols \n")
    indiv = ''
    protocols = ''
    entry = None
    for dir in trio:
        tmp = dir.split('.')
        ind = tmp[0] + '.' + tmp[1]
        prot = tmp[2]
        if indiv == ind:
            protocols += prot + ','
            entry = indiv + "\t" + protocols
        if indiv != ind:
            if entry is not None:
                entry = entry[:-1] + "\n"
                print("Write : {} on {}/metadata.tsv".format(entry[:-1], hic_dir))
                fh.writelines(entry)
            indiv = ind
            protocols = prot + ','
    entry = entry[:-1] + "\n"
    print("Write : {} on {}/metadata.tsv".format(entry[:-1], hic_dir))
    fh.writelines(entry)
    fh.close()


def make_subdir(trio):
    for indiv in trio:
        sp = indiv.split('.')[1]
        path = hic_dir + sp
        if not os.path.exists(path):
            print("Creation of {} directory".format(path))
            os.system(command='mkdir -p ' + path)
        else:
            print("{} already exists".format(path))


def create_matrice_directory():
    h5_path = 'hic_results/matrix/h5df/'
    metadata = hic_dir + 'metadata.tsv'
    RES_DIC = {1000000 : {}, 500000 : {}, 200000 : {}, 50000 : {}}
    with open(metadata, 'r') as mt:
        for line in mt:
            if line.startswith('trio'):
                ind = line.split("\t")[0]
                prots = line.split("\t")[1].split(",")
                for pt in prots:
                    for k in RES_DIC.keys():
                        if pt not in RES_DIC[k].values():
                            RES_DIC[k][pt.replace('\n', '')] = []
                    ind_dir = ind + '.' + pt.replace('\n', '') + '/'
                    try:
                        for k in RES_DIC.keys():
                            mat_path = []
                            for mat in os.listdir(wdir+ind_dir+h5_path):
                                if re.search(r'{}.matrix.h5'.format(k), mat) is not None:
                                    mat_path.append(wdir+ind_dir+h5_path+mat)
                                    RES_DIC[k][pt.replace('\n', '')] = mat_path
                    except OSError:
                        continue
                    
    return RES_DIC


if __name__ == '__main__':
    # Set Working directory :
    wdir = os.path.dirname(os.path.abspath(__file__)) + '/'

    # Set Hic directories
    try:
        sys.argv[1]
    except IndexError:
        hic_dir = wdir+"hic_studies/"
    else:
        hic_dir = sys.argv[1]
    print("Verifing hic_studies directory exist :")
    if not os.path.exists(hic_dir):
        print("hic_studies directory not found \n"
              "Creation of {}".format(hic_dir))
        os.makedirs(hic_dir)
        print("Done.")
    else:
        print("{} founded.".format(hic_dir))

    # Set metadata file :
    TRIO = set_trio(wdir)
    write_metadata(TRIO)

    # Create individuals subdirectories :
    make_subdir(TRIO)

    # Extract paths of matrices
    matrices = create_matrice_directory()
    
    # Sum all matrices
    for res in matrices.keys():
        for prot in matrices[res].keys():
            mats = " ".join(matrices[res][prot])
            cmd = "hicSumMatrices --matrices {} --outFileName {}{}_{}.h5".format(mats, hic_dir, prot, res)
            
            os.system(command=cmd)
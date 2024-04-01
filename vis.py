import argparse
from pathlib import Path
from visgraph import VisGraph
import matplotlib.pyplot as plt

# set up command line argument parser for file name
parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()
path = Path(args.file)          # example: /mtx/will57.mtx
name = path.name                # example: will57.mtx
ext = name.split('.')[-1]       # example: mtx

B = VisGraph()             # object to hold graph
if (ext == 'mtx'):         # read in .mtx file
    B.from_mtx(path)
    B.layout(prog='sfdp')  # lay out graph nodes in 2D using sdfp algorithm
elif (ext == 'gv'):        # read in .gv (DOT file) or .mtx file
    B.from_gv(path)        # note: this file is assumed to be laid out

# B.mm_vis(linewidth=1)  # easy mode, no need to set up figure
fig, ax = plt.subplots(nrows=1,ncols=1)  # we own figure to control/save plot
fig, ax = B.mm_vis(fig,ax,linewidth=1)  # visualize graph
plt.show()

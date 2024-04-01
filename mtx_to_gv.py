import argparse
from pathlib import Path
from visgraph import VisGraph
parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()
path = Path(args.file)      # example: /mtx/will57.mtx
ext = path.name.split('.')[-1]  # file extension

B = VisGraph()
B.from_mtx(path)       # do not lay out
print(B.string())      # to stdout            

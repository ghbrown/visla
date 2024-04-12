
# To do:
- confirm the selected license is compatible with Graphviz's
- (optionally) visualize only the largest connected component
  - will need to identify said component first (at some additional cost)
- make some examples
  - basic call on file with known name
  - set up and save image with transparent background + different colormap

# Rendering
- options (least to most performant, least to most complicated):
  - matplotlib.pyplot.plt
  - (*using, 1/10 time of matplotlib) matplotlib.collections.LineCollection
  - pyqtgraph
  - vispy

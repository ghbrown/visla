
# To do:
- CSV functionality actually doesn't work
  - would be nice if it didn't need the dimensions at the top (could optionally detect them
    by presence of only one comma)
  - should handle 1 vs 0 indexing
- confirm the selected license is compatible with Graphviz's
- (optionally) visualize only the largest connected component
  - will need to identify said component first (at some additional cost)
- make some examples
  - basic call on file with known name
  - set up and save image with transparent background + different colormap
- pygraphviz -> graph-tool?

# Rendering
- options (least to most performant, least to most complicated):
  - matplotlib.pyplot.plt
  - (*using, 1/10 time of matplotlib) matplotlib.collections.LineCollection
  - pyqtgraph
  - vispy

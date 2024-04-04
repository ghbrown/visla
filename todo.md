
# To do:
- confirm the selected license is compatible with Graphviz's
- (optionally) visualize only the largest connected component
  - will need to identify said component first (at some additional cost)
- improve parser inside of __get_nodes_edges
  - currently it makes up half of runtime
  - would be good to carefully profile to get an idea of what's "slow"
  - easy improvements: get contents inside {}, then remove first couple lines, then combine all lines and split on semicolons
- make some examples
  - basic call on file with known name
  - set up and save image with transparent background + different colormap

# Rendering
- options (least to most performant, least to most complicated):
  - matplotlib.pyplot.plt
  - (*using, 1/10 time of matplotlib) matplotlib.collections.LineCollection
  - pyqtgraph
  - vispy

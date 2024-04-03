
# To do:
- Confirm the selected license is compatible with Graphviz's.
- improve parser inside of __get_nodes_edges
  - get contents inside {}, then remove first couple lines, then combine all lines and split on semicolons

# Rendering
- options (least to most performant, least to most complicated):
  - matplotlib.pyplot.plt
  - (*currently here) matplotlib.collections.LineCollection
  - pyqtgraph
  - vispy

# To do:
- would be nice if CSV didn't need the dimensions at the top (could optionally detect them by presence of only one comma)
- confirm the selected license is compatible with Graphviz's
- (optionally) visualize only the largest connected component
  - will need to identify said component first (at some additional cost)
  - can use NetworkX to get all connected components:
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.connected_components.html

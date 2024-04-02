
# To do:
- check licensing stuff, possibly switch license
- scipy.io.mmread() makes one parser irrelevant (take chance to implement pipeline
  from COO to a pygraphvis via loop over rows/cols and add_edge)
- implement wrap around AGraph(<file>) as suggested in readme
- read scipy sparse matrices (COO only, users can convert the rest with Scipy tools)
- see if matplotlib rendering can be done faster (less for looping at least)

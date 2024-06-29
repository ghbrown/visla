
## `visla`
Easy and attractive visualizations of sparse matrices and graphs.

### Samples
![](data/images/grid1_dual.png)
![](data/images/M10PI_n.png)


### Usage
`visla` is a command line program to visualize graphs in the style of [Yifan Hu's Gallery of Large Graphs](http://yifanhu.net/GALLERY/GRAPHS/index.html).

The two figures above were generated with
```
visla grid1_dual.mtx
visla M10PI_n.mtx
```

`visla` accepts a variety of input formats including: Matrix Market, CSV, npz (saved by `scipy.sparse.save_npz`), dot/gv.
You can try it out on the small matrices in `matrices/`.

If you want more fine grained control (like a custom colormap) use the `visla.VGraph` class (documentation below) in a Python program.


### Installation
Once you've obtained the source code you can install it with pip
```
cd visla
pip install .
```

### Documentation
The `visla` command line program has a help message; the rest of this section is dedicated to highlighting the `visla.VGraph` class.
The user is encouraged to read the source code as necessary.

`visla` is powered by an extension of [PyGraphviz's](https://pygraphviz.github.io/documentation/stable/) `AGraph` class.
Specifically, the following methods and fields have been added:
- `from_file()`: read in graph from a file, currently supporting:
  - `mtx`: [Matrix Market](https://math.nist.gov/MatrixMarket/formats.html)
  - `csv`: comma separated values (first line dimensions, rest of lines `i, j, A_ij`)
  - `npz`: npz files saved by [`scipy.sparse.save_npz`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.save_npz.html)
  - `gv/dot`: Graphviz [dot language](https://graphviz.org/docs/outputs/canon/) files 
- `visualize()`: visualize a laid out graph; creates, shows, and destroys its own figure by default, but may be called as `visualize(fig,ax)` if you want control of the figure (for example to use `savefig()`)
- `bg_color`: color of background
- `cm`: color map taking `edge length -> edge color`
- `bipartite`: visualize the bipartite graph corresponding to the sparse matrix (useful for non-square matrices)

See `bin/visla` to see how some of these options are used in practice.


### Notes

- I suggest using some sort of "SuiteSparse-getter" like [`ssgetpy`](https://github.com/drdarshan/ssgetpy) (available via pip) to retrieve `.mtx` files before feeding them to `visla`.

- A few `.mtx` files are included: `will57.mtx` is small and good for prototyping, `grid1_dual.mtx` and `M10PI_n.mtx` are used to generate the figures above.

- Graphs with about 40000 nodes and 130000 edges can be visualized in under 2 minutes on a laptop.


### Sources

The pipeline to create these visualization was informed by the following:
- [Yifan Hu's Gallery of Large Graphs](http://yifanhu.net/GALLERY/GRAPHS/index.html)
- [Tim Davis's synopsis of how Yifan Hu generated his figures](https://people.engr.tamu.edu/davis/matrices.html)

Some interesting facts learned along the way:
- edges are colored according to their lengths
- these visualizations are only in two dimensions


### Limitations

- Currently all connected components are visualized, but ideally one could (optionally) visualize only the largest component.
- The parser to get connectivity and coordinates was made to work on practical examples.
  I don't know of any cases where it fails, but be wary.

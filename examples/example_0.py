from visla import VGraph
import matplotlib.pyplot as plt

# set up and layout graph
B = VGraph()                            # object to hold graph
B.from_file('../matrices/M10PI_n.mtx')  # read in graph
B.layout(prog='sfdp')                   # lay out graph nodes in 2D using sdfp algorithm
B.colormap = plt.get_cmap("turbo")      # set colormap

# visualize
fig, ax = plt.subplots(nrows=1,ncols=1)  # create figure to control/save plot
fig, ax = B.visualize(fig,ax)            # visualize graph
plt.show()
fig.savefig('M10PI_n.png',               # save to file
            dpi=300,transparent=True)

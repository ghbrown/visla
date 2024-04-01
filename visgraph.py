from icecream import ic
from pygraphviz import AGraph
from numpy import array
from numpy.linalg import norm
import matplotlib.pyplot as plt
import cmasher as cmr

class VisGraph(AGraph):
    def __init__(self):
        AGraph.__init__(self,strict=True,directed=False)
        self.__layout_lines = []  # output of layout() as lines of file
        self.__nodes = {}
        self.__edges = []
        self.bg_color = 'black'
        self.cm       = cmr.get_sub_cmap(cmr.chroma,0.5,0.8)

    def layout(self,prog='sfdp',args=''):
        """
        standard AGraph.layout(), except default to faster sfdp algorithm
        also set up internal variable from which positions are extracted
        """
        AGraph.layout(self,prog=prog,args=args)
        self.__layout_lines = self.__multiline_to_lines(self.string())

    def from_mtx(self,file_name):
        """
        set up a GraphViz graph from a .mtx file
        """
        # set up reasonable defaults
        self.node_attr["label"] = 'ugh'  # PGV broken relative to GV
        self.node_attr["shape"] = "none"
        self.node_attr["width"] = 0
        self.node_attr["height"] = 0
        self.edge_attr["penwidth"] = 1
        # put edges into graph
        with open(file_name) as f:
            lines = f.readlines()
        i_last = 0 # last line containing break (%----)
        for i_l, line in enumerate(lines):
            if ('%---' in line):
                i_last = i_l
        i_dim = i_last + 1 # contains dimensions
        i_0 = i_dim + 2    # first line containing data
        for line in lines[i_0:]:
            i, j = line.strip().split()[0:2]  # ingore nonzero (if present)
            self.add_edge(i,j)

    def from_gv(self,file_name):
        """
        set up for visualization using .gv file with layout information (nodal
        positions
        note: does not construct a GraphViz graph
        """
        with open(file_name) as f:
            lines = f.readlines()
        self.__layout_lines = [line.strip() for line in lines if line.strip()]

    def __multiline_to_lines(self,ml):
        # https://stackoverflow.com/questions/7630273/convert-multiline-into-list
        lines = [y for y in (x.strip() for x in ml.splitlines()) if y]
        return lines

    def __get_nodes_edges(self,lines):
        """
        get nodes dictionary and edges list from list of lines formatted as
        standard .gv output (i.e. like output of `neato graph.gv`)
        """
        def until_next(lines,char):
            cur_lines = []
            for line in lines:
                if (char not in line):
                    cur_lines.append(line)
                else:  # char is in line
                    cur_lines.append(line)
                    break
            return cur_lines

        def read_node(lines):
            # lines will be representative of a single .gv node
            i = 0
            # get node label
            label = lines[0].strip().split()[0] # first nonspace object is label
            for line in lines:
                if ('pos' in line):
                    middle = line.strip().split('"')[1]  # get "<stuff in here>"
                    p = array([float(a) for a in middle.split(',')])
            return label, p

        def read_edge(lines):
            # lines will be representative of a single .gv edge
            label_l, label_r = lines[0].strip().replace('--',' ').split()[0:2]
            return label_l, label_r

        # tabs -> spaces, remove lines with { or }
        lines = [line.replace('\t',' ') for line in self.__layout_lines
                if (('{' not in line) and ('}' not in line))]

        # find end of header / start of nodes and edges
        i_ne = 0
        done = False
        while (not done):
            header_words = ['graph', 'node', 'edge']
            token = until_next(lines[i_ne:],';') # multi-line token
            token_joined = ' '.join([l.strip() for l in token])
            if any(word in token_joined for word in header_words):
                i_ne += len(token)   # token may be multiple lines
            else:
                done = True

        lines = lines[i_ne:] # drop all header lines

        # read in nodes and edges
        i = 0
        while (i < len(lines)):
            token = until_next(lines[i:],';') # multi-line token
            if ('--' in token[0]):  # edge
                label_l, label_r = read_edge(token)  # two labels
                self.__edges.append([label_l,label_r])
            else:  # node
                label, x = read_node(token)  # label and position
                self.__nodes[label] = x
            i += len(token)   # token may be multiple lines
        
    def mm_vis(self,fig=None,ax=None,*args,**kwargs):
        """
        visualizes the graph in the style of:
          - Yifan Hu's gallery of large graphs
            (http://yifanhu.net/GALLERY/GRAPHS/index.html)
        fig: user figure on which to plot
        ax : user axis on which to plot
        if fig, ax are supplied they are passed back to the user
        if the caller does not supply a fig/ax, we create and show our own
           figure
        """
        if (not self.__layout_lines):
            raise Exception('the graph has not been laid out yet; layout an existing PyGraphVis graph with .layout() or read in node positions and edges of a laid out graph file with .read_gv()')
        self.__get_nodes_edges(self.__layout_lines)

        # determine if user has passed their own plot object or if we should
        # create our won
        ez_plot = ((fig is None) or (ax is None))

        # get max edgelength
        d_max = 0
        for (label_1, label_2) in self.__edges:
            n_1 = self.__nodes[label_1]
            n_2 = self.__nodes[label_2]
            d_cur = norm(n_1-n_2)
            if (d_cur > d_max):
                d_max = d_cur

        # render
        if (ez_plot):  # we can create and destroy our own plot
            fig, ax = plt.subplots(nrows=1,ncols=1)
        fig.patch.set_facecolor(self.bg_color)
        ax.patch.set_facecolor(self.bg_color)
        for (label_1, label_2) in self.__edges:
            n_1 = self.__nodes[label_1]
            n_2 = self.__nodes[label_2]
            x = [n_1[0], n_2[0]]
            y = [n_1[1], n_2[1]]
            ax.plot(x,y,
                    **kwargs,
                    color = self.cm(norm(n_1 - n_2)/d_max))
        ax.axis('square')
        ax.axis('off')
        if (ez_plot):      # show plot for user
            plt.show()
        else:              # give user control over plot
            return fig, ax

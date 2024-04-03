from pathlib import Path
from numpy import array, empty
from numpy import max as nmax
from numpy.linalg import norm
from scipy.io import mmread
from scipy.sparse import isspmatrix_coo, coo_matrix, load_npz
from pygraphviz import AGraph
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import cmasher as cmr

class VGraph(AGraph):
    def __init__(self):
        AGraph.__init__(self,strict=True,directed=False)
        self.__layout_lines = []  # output of layout() as lines of file
        self.__nodes = {}
        self.__edges = []
        # files with __from_<extsion>
        self.__impl_files = ['csv', 'mtx', 'npz', 'dot', 'gv']
        self.bg_color = 'black'
        self.cm       = cmr.get_sub_cmap(cmr.tropical,0.0,1.0)
        self.bipartite = None

    def layout(self,prog='sfdp',args=''):
        """
        standard AGraph.layout(), except default to faster sfdp algorithm
        also set up internal variable from which positions are extracted
        """
        AGraph.layout(self,prog=prog,args=args)
        self.__layout_lines = self.__multiline_to_lines(self.string())

    def from_file(self,file_name,file_type=None):
        """
        set up a GraphViz graph from a .mtx file
        """
        _file_type = None  # will be a legal file type
        # ensure we can parse the (implicitly) requested file type
        if (file_type is not None):
            if (file_type not in self.__impl_files):
                raise Exception(f'file type {file_type} is unsupported',
                                'legal file types are {self.__impl_files}')
            else:  # file type selection valid
                _file_type = file_type
        else: # we'll have to guess the file type from extension
            ext = Path(file_name).name.split('.')[-1]
            if (ext not in self.__impl_files):
                raise Exception(f'file type {file_type} is unsupported',
                                f'try using the file_type option to force parsing as a file_type file')
            else:  # file type selection valid
                _file_type = ext

        # set up reasonable defaults
        # self.node_attr["label"] = ""  # PyGraphviz doesn't like this
        self.node_attr["shape"] = "none"
        self.node_attr["width"] = 0
        self.node_attr["height"] = 0
        self.edge_attr["penwidth"] = 1
        
        # __from_<extension> functions expected to set graph up themselves
        if   (_file_type == 'mtx'):
            self.__from_mtx(file_name) 
        elif (_file_type == 'csv'):
            self.__from_csv(file_name)
        elif (_file_type == 'npz'):
            self.__from_npz(file_name)
        elif (_file_type in ['dot','gv']):
            self.__from_gv(file_name)

    def __from_csv(self,file_name):
        """
        set up a graph from a CSV file with 3 rows
        first row must contain dimensions
        """
        with open(file_name) as f:
            lines = f.readlines()
        # get dimensions from first line
        m, n = [int(a.strip()) for a in lines[0].strip().split(',')[0:2]]
        # get connectivity data from following lines
        row = empty(len(lines)-1,dtype=int)  # -1 since first line has dimensions
        col = empty(row.shape[0],dtype=int)
        for i_l, line in enumerate(lines[1:]):
            row[i_l], col[i_l] = [int(a.strip()) for a in
                                  line.strip().split(',')[0:2]]
        data = empty(row.shape[0])  # dummy values, have no impact
        A = coo_matrix((data,(row,col)),shape=(m,n))
        self.__graph_from_coo(A)

    def __from_npz(self,file_name):
        """
        set up graph from an npz file containing a sparse matrix
        """
        A = load_npz(file_name)
        if (not isspmatrix_coo(A)):
            A = A.asformat('coo')
        self.__graph_from_coo(A)

    def __from_mtx(self,file_name):
        """
        set up graph from an mtx file
        """
        A = mmread(file_name)  # A is COO by default
        self.__graph_from_coo(A)

    def __from_gv(self,file_name):
        """
        set up graph from a dot/gv file
        https://graphviz.org/docs/outputs/canon/
        """
        self.read(file_name)

    def __graph_from_coo(self,A):
        """
        builds a GraphVis graph from a scipy.sparse.coo_matrix
        """
        m, n = A.shape  # row and column dimensions
        # construct list containing edges of the graph to be visualized
        # all edges "start at i", but in the bipartite case we suppose the
        # sparse matrix corresponds to a graph with m + n nodes and that the
        # terminus of the (i,j) entry from the graph is actually (i,m+j)
        i_str = [str(i) for i in A.row]
        # determine whether graph should be bipartite
        _bipartite = None
        if (self.bipartite is None):  # user trusts us to choose
            _bipartite = (m != n)
        else:
            _bipartite = self.bipartite
        # set up graph
        if (_bipartite):  # bipartite graph
            j_str = [str(m+j) for j in A.col]
        else:             # graph corresponding to A + A^T
            j_str = [str(j) for j in A.col]
        edge_list = [[i,j] for i, j in zip(i_str,j_str)]
        self.add_edges_from(edge_list)  # put edges into graph

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
        
    def visualize(self,fig=None,ax=None,*args,**kwargs):
        """
        visualizes the graph in the style of:
          - Yifan Hu's gallery of large graphs
            (http://yifanhu.net/GALLERY/GRAPHS/index.html)
        fig: user figure on which to plot
        ax : user axis on which to plot
        if fig, ax are supplied they are passed back to the user
        if caller does not supply a fig/ax, we create and show our own figure
        """
        if (not self.__layout_lines):
            raise Exception('the graph has not been laid out yet; layout an existing PyGraphVis graph with .layout() or read in node positions and edges of a laid out graph file with .read_gv()')
        self.__get_nodes_edges(self.__layout_lines)

        # determine if user has passed their own plot object or if we should
        # create our own
        ez_plot = ((fig is None) or (ax is None))

        # get max edgelength
        d_max = 0
        for (label_1, label_2) in self.__edges:
            n_1 = self.__nodes[label_1]
            n_2 = self.__nodes[label_2]
            d_cur = norm(n_1-n_2)
            if (d_cur > d_max):
                d_max = d_cur

        # prepare to render (create figure, set up LineCollection)
        if (ez_plot):  # we can create and destroy our own plot
            fig, ax = plt.subplots(nrows=1,ncols=1)
        fig.patch.set_facecolor(self.bg_color)
        ax.patch.set_facecolor(self.bg_color)
        # dimensions of segments: number of lines x points per line x dimension
        segments = empty((len(self.__edges),2,2),dtype='float64')
        colors   = [self.cm(0)]*segments.shape[0]  # color of each segment
        for i_l, (label_1, label_2) in enumerate(self.__edges):
            n_1 = self.__nodes[label_1]
            n_2 = self.__nodes[label_2]
            segments[i_l] = array([n_1,n_2])
            colors[i_l] = self.cm(norm(n_1 - n_2)/d_max)

        # render
        line_segments = LineCollection(segments,*args,colors=colors,**kwargs)
        ax.add_collection(line_segments)
        ax.axis('square')
        ax.axis('off')
        if (ez_plot):      # show plot for user
            plt.show()
        else:              # give user control over plot
            return fig, ax

    def __multiline_to_lines(self,ml):
        # https://stackoverflow.com/questions/7630273/convert-multiline-into-list
        lines = [y for y in (x.strip() for x in ml.splitlines()) if y]
        return lines

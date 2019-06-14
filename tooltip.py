import matplotlib.pyplot as plt
import numpy as np; np.random.seed(1)

class Popgraph:

    def __init__(self,data,x,y,type = 'scatter',low_xlim=None,low_ylim=None,high_xlim=None,high_ylim=None):
        self.data = data
        self.xlabel,self.x = x,data[x]
        self.ylabel,self.y = y,data[y]
        self.high_xlim = high_xlim
        self.low_xlim = low_xlim
        self.high_ylim = high_ylim
        self.low_ylim = low_ylim
        if not self.low_xlim:
            self.low_xlim = self.x.min()
        if not self.low_ylim:
            self.low_ylim = self.y.min()
        if not self.high_xlim:
            self.high_xlim = self.x.max()
        if not self.high_ylim:
            self.high_ylim = self.y.max()

        self.names = np.array(list(self.data['Store']))
        self.c = np.random.randint(1,5,size=len(self.names))

        self.norm = plt.Normalize(1,4)
        self.cmap = plt.cm.RdYlGn

        self.fig,self.ax = plt.subplots()

        self.sc = plt.scatter(self.x,self.y,c=self.c, s=50, cmap=self.cmap, norm=self.norm)

        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))

        self.annot.set_visible(False)

        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.xlim(float(self.low_xlim),float(self.high_xlim))
        plt.ylim(float(self.low_ylim),float(self.high_ylim))

        plt.show()


    def update_annot(self,ind):
        pos = self.sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        text = "Store_No: {}\n{}: {}\n{}: {}".format(" ".join([self.names[n] for n in ind["ind"]]),
                                                      self.xlabel,
                                                      " ".join(str(round(self.x.iloc[n],5)) for n in ind['ind'] ),
                                                      self.ylabel,
                                                      " ".join(str(round(self.y.iloc[n],5)  ) for n in ind['ind'])
                                                      )
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_facecolor(self.cmap(self.norm(self.c[ind["ind"][0]])))
        self.annot.get_bbox_patch().set_alpha(0.4)

    def hover(self,event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.sc.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()

from tkinter import messagebox, filedialog, ttk
from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.backends.backend_tkagg as tkagg

'''
Owner: sachin.prabhu
Last Edited Date: 02-Aug-2019
'''


class Vizboard():
    def __init__(self,master):

        self.docstring ='''
Viz Board is a tool meant for flexible visualization of Big Data.
This can essential connect to any data source which provides flexible API.
As of now, Viz Board provides data connectivity to excel and csv files.

Note: Excel and csv dumps from DSS needs to be brought to normal format before importing into this tool.

In case of queries, please connect with sachin.prabhu.
        '''

        #setting master properties
        master.title('Viz Board')
        master.geometry("1080x720")
        master.option_add('*tearOff', False)
        master.protocol('WM_DELETE_WINDOW', lambda: self.ask_quit(master))
        #binding keys
        master.bind_all('<Return>', lambda e: self.pack_graph(master))
        master.bind_all('<Control-q>',lambda e:master.destroy())
        master.bind_all('<Control-o>',lambda e:self.get_file(master))
        # master.configure(background = 'gray')

        #create a toplevel menu
        menubar = Menu(master)
        file = Menu(menubar)
        menubar.add_cascade(label='File',menu=file)
        file.add_command(label='Open',command = lambda:self.get_file(master), accelerator = 'Ctrl+O')
        file.add_separator()
        file.add_command(label='Exit',command = lambda : master.destroy(), accelerator = 'Ctrl+Q')
        menubar.add_command(label ='About', command = lambda : self.show_help())
        master.config(menu=menubar)

        #frame decs
        file_frame = ttk.Frame(master)
        #options_frame = ttk.Frame(master) #yet to pack

        #widget decs
        self.path_entry = ttk.Entry(file_frame, width=100)
        open_btn = ttk.Button(file_frame, text = 'Open', command = lambda: self.get_file(master))
        clear_btn = ttk.Button(file_frame, text = 'Clear', command = lambda: self.clear())
        clear_graph_button = ttk.Button(file_frame, text = 'Clear Graphs', command = lambda: self.clear_graph())

        #widget pack
        ttk.Label(file_frame,text='Path:').grid(row=0,column=0,padx=2,pady=2)
        self.path_entry.grid(row=0,column=1,padx=2,pady=2)
        open_btn.grid(row=0, column=2,padx=2,pady=2)
        clear_btn.grid(row=0, column=3,padx=2,pady=2)
        clear_graph_button.grid(row=0, column=4, padx=2,pady=2)

        #frame pack
        file_frame.pack()


    def ask_quit(self,master):
        #called when user quits through close on title bar
        if messagebox.askokcancel('Quit', 'Are you sure?'):
            plt.close()
            master.quit()

    def read_file(self,path):
        #called from get_file
        try:
            if '.csv' in path:
                data = pd.read_csv(path)
                return data
            elif '.xls' in path or '.xlsx' in path:
                data = pd.read_excel(path)
                return data
        except FileNotFoundError:
            messagebox.showerror(title = 'Error', message = 'Incorrect/Blank path!')

    def get_file(self,master):
        #invoked once user clicks on 'open' button on UI.
        try: # checks if user provided path for input data
            self.path = self.path_entry.get()
            if self.path:
                self.data = pd.read_csv(str(self.path))
            else: #else opens up a file dialog
                self.path = filedialog.askopenfilename(initialdir = '/home/linux_fed/Desktop', title = 'select file',
                filetypes = (('excel file','*.xlsx'),('csv files','*.csv')))
                self.data = self.read_file(self.path)
                self.path_entry.insert(0,str(self.path))
            self.get_options(master)
        except AttributeError as e:
            print('at get_file '+str(e)) #for testing.
            #messagebox.showerror(title = 'Error',message = 'No file selected!')

        except FileNotFoundError:
            messagebox.showerror(title='Error', message = 'Incorrect/Blank Path')

    def get_options(self,master):
        #called from within get_file function

        #for column dropdowns and plot buttons
        self.options_frame = ttk.Frame(master)
        self.buttons_frame = ttk.Frame(master)

        columns = list(self.data.columns)

        #column 1 for X
        self.tkvar1 = StringVar(master)

        #columns = [column for column in self.data.columns if self.data[column].dtype == 'int64' or self.data[column].dtype == 'float64' ] #takes only numeric values
        self.tkvar1.set("Select")
        self.column_drop = OptionMenu(self.options_frame,self.tkvar1,*columns)
        ttk.Label(self.options_frame,text = 'X:').grid(row=0,column=0,sticky=E,padx=2,pady=2)
        self.column_drop.grid(row=0,column=1,sticky=E,padx=2,pady=2)

        #column 2 for Y; needs to be numeric
        self.tkvar2 = StringVar(master)
        columns = [column for column in self.data.columns if self.data[column].dtype == 'int64' or self.data[column].dtype == 'float64'] #takes only numeric values
        self.tkvar2.set("Select")
        self.column_drop = OptionMenu(self.options_frame,self.tkvar2,*columns)
        ttk.Label(self.options_frame,text = 'Y:').grid(row=0,column=2,padx=2,pady=2)
        self.column_drop.grid(row=0,column=3,padx=2,pady=2)

        #column for label_tooltip_V2
        self.tkvar3 = StringVar(master)
        columns = list(self.data.columns)
        self.tkvar3.set(columns[2])
        self.column_drop = OptionMenu(self.options_frame,self.tkvar3,*columns)
        self.label_dropdown = ttk.Label(self.options_frame, text = 'Label')
        self.label_dropdown.grid(row=0,column=12,padx=2,pady=2)
        self.column_drop.grid(row=0,column=13,padx=2,pady=2)

        #lower lims for x and y
        self.low_xlabel = ttk.Label(self.options_frame, text = 'Lower limit {}: '.format(self.tkvar1.get()))
        self.low_xlabel.grid(row=0,column=4,padx=2,pady=2)
        self.low_xlim_entry = ttk.Entry(self.options_frame)
        self.low_ylabel = ttk.Label(self.options_frame,text = 'Lower limit {}: '.format(self.tkvar2.get()))
        self.low_ylabel.grid(row=0,column=8,padx=2,pady=2)
        self.low_ylim_entry = ttk.Entry(self.options_frame)
        self.low_xlim_entry.grid(row=0,column=5)
        self.low_ylim_entry.grid(row=0,column=9)

        #higher lims for x and y
        self.high_xlabel = ttk.Label(self.options_frame, text = 'Higher limit {}: '.format(self.tkvar1.get()))
        self.high_xlabel.grid(row=0,column=6,padx=2,pady=2)
        self.high_xlim_entry = ttk.Entry(self.options_frame)
        self.high_ylabel = ttk.Label(self.options_frame,text = 'Higher limit {}: '.format(self.tkvar2.get()))
        self.high_ylabel.grid(row=0,column=10,padx=2,pady=2)
        self.high_ylim_entry = ttk.Entry(self.options_frame)
        self.high_xlim_entry.grid(row=0,column=7)
        self.high_ylim_entry.grid(row=0,column=11)


        #buttons for graphs
        self.scatter_btn = ttk.Button(self.buttons_frame,text = 'Scatter Plot', state = DISABLED,
                                     command = lambda : self.pack_graph(master,'scatter')
                                     )
        self.line_btn = ttk.Button(self.buttons_frame,text = 'Line Plot',state = DISABLED,
                                     command = lambda : self.pack_graph(master,'line')
                                     )


        self.bar_btn = ttk.Button(self.buttons_frame,text = 'Bar Plot',state = DISABLED,
                                  command = lambda : self.pack_graph(master,'bar')
                                  )

        self.pie_btn = ttk.Button(self.buttons_frame,text = 'Pie Plot',state = DISABLED,
                                  command = lambda : self.pack_graph(master,'pie')
                                  )


        #packing buttons
        self.scatter_btn.grid(row=0,column=0,padx=2,pady=2)
        self.line_btn.grid(row=0,column=1,padx=2,pady=2)
        self.bar_btn.grid(row=0, column=2, padx=2, pady=2)
        self.pie_btn.grid(row=0, column=3, padx=2, pady=2)


        #packing frames that are supposed to pack programmatically
        self.options_frame.pack(anchor='center', padx=10, pady=10)
        self.buttons_frame.pack(anchor='center', padx=10, pady=10)


        #tracing changes in columns
        self.tkvar1.trace('w',self.change_label)
        self.tkvar2.trace('w',self.change_label)






    def clear(self):
        #called through self.clear_btn
        if messagebox.askokcancel('Clear', 'You are about to clear all data!'):
            try:
                    self.path_entry.delete(0,'end')
                    self.options_frame.pack_forget()
                    self.options_frame.destroy()
                    self.buttons_frame.pack_forget()
                    self.buttons_frame.destroy()
                    self.options_frame.pack_forget()
                    self.options_frame.destroy()
                    self.graphs_frame.pack_forget()
                    self.graphs_frame.destroy()
            except AttributeError as e: #in case user hits clear before frames are populated
                # print('at clear '+str(e)) #for testing. pass this
                pass

    def clear_graph(self):
        #called through self.clear_graph_button as well as from pack_graph
        try:
            self.graphs_frame.pack_forget()
            self.graphs_frame.destroy()
            self.canvas.get_tk_widget().destroy()
        except AttributeError as e:
            # print('at clear_graph '+str(e))# for testing
            messagebox.showifo(title = '!', message = 'Nothing to clear!')

    def show_help(self):
        messagebox.showinfo(title = 'About',message = self.docstring)

    def change_label(self,*args): #this changes the limit value labels based on OptionMenu
        try:
            x_col = self.tkvar1.get()
            y_col = self.tkvar2.get()

            # low labels
            self.low_xlabel.config(text='')
            self.low_xlabel.config(text='Lower limit {}:'.format(x_col))

            self.low_ylabel.config(text='')
            self.low_ylabel.config(text='Lower limit {}:'.format(y_col))

            #high labels
            self.high_xlabel.config(text='')
            self.high_xlabel.config(text='Higher limit {}:'.format(x_col))

            self.high_ylabel.config(text='')
            self.high_ylabel.config(text='Higher limit {}:'.format(y_col))

            print(self.data[x_col].dtype)
            print(self.data[y_col].dtype)

            #updating button states based
            #if both columns are numeric, enabling scatter only.
            if (self.data[x_col].dtype == np.dtype('int64') or  self.data[x_col].dtype == np.dtype('float64')) and (self.data[y_col].dtype == np.dtype('int64') or self.data[y_col].dtype == np.dtype('float64')):
                print('scatter should be enabled')
                self.scatter_btn.configure(state = NORMAL)
                self.bar_btn.configure(state = DISABLED)
                self.line_btn.configure(state = DISABLED)
                # self.dot_btn.configure(state = DISABLED)
                self.low_xlim_entry.configure(state=NORMAL)
                self.high_xlim_entry.configure(state=NORMAL)
                self.label_dropdown.configure(state=NORMAL)
            #if x-axis is of object type, disabling scatter
            if (self.data[x_col].dtype == 'object' or self.data[x_col].dtype == np.dtype('datetime64') or self.data[x_col].dtype == np.dtype('<M8[ns]')) and (self.data[y_col].dtype == np.dtype('int64') or self.data[y_col].dtype == np.dtype('float64')):
                print('scatter should be disabled')
                self.scatter_btn.configure(state = DISABLED)
                self.bar_btn.configure(state = NORMAL)
                self.line_btn.configure(state = NORMAL)
                # self.dot_btn.configure(state = NORMAL)
                self.low_xlim_entry.configure(state=DISABLED)
                self.high_xlim_entry.configure(state=DISABLED)
                self.label_dropdown.configure(state=NORMAL)

            #enabling pie-button only if sum of y is 1

            if (self.data[y_col].dtype == np.dtype('int64') or self.data[y_col].dtype == np.dtype('float64')) and self.data[y_col].sum()==1:
                self.pie_btn.configure(state = NORMAL)
                self.label_dropdown.configure(state=DISABLED)
        except KeyError:
            pass # if user doesn't change the default value



    def pack_graph(self,master,type = 'scatter'):


        #setting up default params
        data=self.data
        self.xlabel = self.tkvar1.get()
        self.ylabel = self.tkvar2.get()
        self.x = data[self.xlabel]
        self.y = data[self.ylabel]
        self.label_col = self.tkvar3.get()
        self.type = type


        try:
            self.clear_graph() #checking if a graph is already populated
            plt.clf()
        except AttributeError as e:
            # print('at pack_graph '+str(e)) #for testing only. This is supposed to throw AttributeError on the first run
            pass

        #setting up the graph properties
        low_ylim = self.low_ylim_entry.get()
        high_ylim = self.high_ylim_entry.get()
        if not high_ylim:
            high_ylim = self.y.max()
        if not low_ylim:
            low_ylim = self.y.min()

        if not self.label_col:
            self.label_col = data[self.xlabel]

        self.names = np.array(list(data[self.label_col])) #creating a numpy array list from label_col
        self.c = np.random.randint(1,5,size=len(self.names)) #for picking random color
        self.norm = plt.Normalize(1,5) #for normalizing luminance data
        self.cmap = plt.cm.Greens
        self.fig, self.ax = plt.subplots()
        self.graphs_frame = ttk.Frame(master)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphs_frame)# A tk.DrawingArea.
        tkagg.NavigationToolbar2Tk(self.canvas, self.graphs_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=X)
        self.graphs_frame.pack(fill=X)

        plt.title('{} vs {}'.format(self.xlabel.upper(), self.ylabel.upper()))
        plt.xlabel(self.xlabel.title())
        plt.ylabel(self.ylabel.title())
        plt.ylim(float(low_ylim),float(high_ylim))


        #setting up properties for different type of graphs
        if self.type == 'scatter':
            low_xlim = self.low_xlim_entry.get()
            high_xlim = self.high_xlim_entry.get()
            if not high_xlim:
                high_xlim = self.x.max()
            if not low_xlim:
                low_xlim = self.x.min()
            plt.xlim(float(low_xlim), float(high_xlim))
            self.sc = plt.scatter(self.x,self.y,c=self.c, s=50, cmap=self.cmap, norm=self.norm)

        elif self.type == 'line':
            self.x = self.x.astype('object')
            self.pos = np.arange(len(self.y))
            self.sc = plt.plot(self.pos,self.y)
            plt.xticks(self.pos, self.x)

        elif self.type == 'bar':
            self.x = self.x.astype('object')
            pos = np.arange(len(self.y))
            self.sc = plt.bar(pos,self.y, width = 0.8)
            plt.xticks(pos, self.x)

        elif self.type == 'pie':
            self.sc = plt.pie(self.y, labels = self.x)
            plt.title(self.ylabel)
            plt.xlabel('')
            plt.ylabel('')
            messagebox.showinfo(title = 'Info', message = 'Pie takes X column as label column, changes label column will not affect the pie graph.')

        '''else:
            self.x = self.x.astype('object')
            self.pos = np.arange(len(self.y))
            self.sc = plt.plot(self.pos,self.y, 'ro')
            plt.xticks(self.pos, self.x)
            self.type = 'line' '''

        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))

        self.annot.set_visible(False)

        self.canvas.mpl_connect("motion_notify_event", self.hover)


        #plt.show()


    def update_annot(self,event,ind):
        if self.type == 'scatter':
            pos = self.sc.get_offsets()[ind["ind"][0]] # positions of the tooltip
            self.annot.xy = pos
            text = "{}: {}\n{}: {}\n{}: {}".format(self.label_col,
                                                          " ".join(str(self.names[n]) for n in ind["ind"]),
                                                          self.xlabel,
                                                          " ".join(str(round(self.x.iloc[n],5)) for n in ind['ind'] ),
                                                          self.ylabel,
                                                          " ".join(str(round(self.y.iloc[n],5)  ) for n in ind['ind'])
                                                          )
            self.annot.set_text(text)
            self.annot.get_bbox_patch().set_facecolor(self.cmap(self.norm(self.c[ind["ind"][0]])))
            self.annot.get_bbox_patch().set_alpha(0.4)

        elif self.type == 'bar':
                x= ind.get_x()+ind.get_width()/2
                y = ind.get_y()+ind.get_height()
                self.annot.xy = event.xdata, event.ydata
                # print(x) #for testing
                text = "{}:{}\n{}: {}".format(self.label_col, str(self.names[int(x)]), self.ylabel, y)
                self.annot.set_text(text)
                self.annot.get_bbox_patch().set_alpha(0.4)

        elif self.type == 'line':
                x, y = event.xdata, event.ydata
                # x,y = ind.get_xdata()[int(event.xdata)], ind.get_ydata()[int(event.ydata)] #needs to be changed
                self.annot.xy = x, y
                coords = ind.get_xydata()[int(x)]
                print(coords[0])
                text = "{}:{}\n{}:{}".format(self.label_col, self.names[int(coords[0])], self.ylabel, str(self.y[int(coords[0])]))
                # print('X: ', x)
                # print('Y: ', y)
                # print('XY_DATA', ind.get_xydata())
                self.annot.set_text(text)
                self.annot.get_bbox_patch().set_alpha(0.4)


    def hover(self,event):
        #on hover listener for tooltip

        if self.type == 'scatter':
            vis = self.annot.get_visible()
            if event.inaxes == self.ax:
                cont, ind = self.sc.contains(event)
                if cont:
                    self.update_annot(event,ind)
                    self.annot.set_visible(True)
                    self.fig.canvas.draw_idle()
                else:
                    if vis:
                        self.annot.set_visible(False)
                        self.fig.canvas.draw_idle()

        elif self.type == 'bar':
                vis = self.annot.get_visible()
                if event.inaxes == self.ax:
                    for bar in self.sc:
                        cont, ind = bar.contains(event)
                        if cont:
                            self.update_annot(event,bar)
                            self.annot.set_visible(True)
                            self.fig.canvas.draw_idle()
                            return
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()

        elif self.type == 'line':
            vis = self.annot.get_visible()
            if event.inaxes == self.ax:
                for line in self.sc:
                    cont, ind = line.contains(event)
                    if cont:
                        print('ind', ind)
                        self.update_annot(event,line)
                        self.annot.set_visible(True)
                        self.fig.canvas.draw_idle()
                        return
            if vis:
                self.annot.set_visible(False)
                self.fig.canvas.draw_idle()




def main():
    root = Tk()
    vizboard = Vizboard(root)
    # root.style = ttk.Style()
    #('clam', 'alt', 'default', 'classic')
    # root.style.theme_use("clam")

    root.mainloop()
    plt.close()

if __name__=='__main__':
    main()

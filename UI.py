from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import tooltip

class Vizboard:

    def __init__(self,master):


        #create a toplevel menu
        menubar = Menu(master)
        file = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='File',menu=file)
        file.add_command(label='Open',command = lambda:self.get_file(master), accelerator = 'Ctrl+O')
        file.add_separator()
        file.add_command(label='Exit',command = lambda : master.destroy(), accelerator = 'Ctrl+Q')
        menubar.add_command(label ='About', command = lambda : self.show_help(master))

        master.config(menu=menubar)
        #frame decs
        file_frame = ttk.Frame(master)
        #options_frame = ttk.Frame(master) #yet to pack

        #widget decs
        self.path_entry = ttk.Entry(file_frame, width=100)
        open_btn = ttk.Button(file_frame, text = 'Open', command = lambda: self.get_file(master))
        clear_btn = ttk.Button(file_frame, text = 'Clear', command = lambda: self.clear())


        #widget pack
        ttk.Label(file_frame,text='Path:').grid(row=0,column=0,padx=2,pady=2)
        self.path_entry.grid(row=0,column=1,padx=2,pady=2)
        open_btn.grid(row=0, column=2,padx=2,pady=2)
        clear_btn.grid(row=0, column=3,padx=2,pady=2)

        #frame pack
        file_frame.pack()

        #binding keys
        master.bind('<Return>', lambda e:self.get_file(master))
        master.bind_all('<Control-q>',lambda e:master.destroy())
        master.bind_all('<Control-o>',lambda e:self.get_file(master))


    def get_file(self,master):
        try:
            self.path = self.path_entry.get()
            if self.path:
                self.data = pd.read_csv(str(self.path))
            else:
                self.path = filedialog.askopenfilename(initialdir = '/home/linux_fed/Desktop', title = 'select file',
                filetypes = (('excel file','*.xlsx'),('csv files','*.csv')))
                self.data = self.read_file(self.path)
                self.path_entry.insert(0,str(self.path))
            self.column_string= ', '.join(list(self.data.columns))
            self.get_options(master)
        except AttributeError:
            messagebox.showerror(title = 'Error',message = 'No file selected!')

    def get_options(self,master):
        #for column dropdowns and plot buttons
        self.options_frame = ttk.Frame(master)
        self.buttons_frame = ttk.Frame(master)


        #column 1 for X
        self.tkvar1 = StringVar(master)
        columns = list(self.data.columns)
        self.tkvar1.set(columns[0])
        self.column_drop = OptionMenu(self.options_frame,self.tkvar1,*columns)
        ttk.Label(self.options_frame,text = 'X:').grid(row=0,column=0,sticky=E,padx=2,pady=2)
        self.column_drop.grid(row=0,column=1,sticky=E,padx=2,pady=2)

        #column 2 for Y
        self.tkvar2 = StringVar(master)
        columns = list(self.data.columns)
        self.tkvar2.set(columns[1])
        self.column_drop = OptionMenu(self.options_frame,self.tkvar2,*columns)
        ttk.Label(self.options_frame,text = 'Y:').grid(row=0,column=2,padx=2,pady=2)
        self.column_drop.grid(row=0,column=3,padx=2,pady=2)
        #self.tkvar2.trace('w',self.change_dropdown)

        #column for label_tooltip

        self.tkvar3 = StringVar(master)
        columns = list(self.data.columns)
        self.tkvar3.set(columns[2])
        self.column_drop = OptionMenu(self.options_frame,self.tkvar3,*columns)
        ttk.Label(self.options_frame, text = 'Label').grid(row=0,column=12)
        self.column_drop.grid(row=0,column=13,padx=2,pady=2)

        #lims for x and y
        ttk.Label(self.options_frame, text = 'Lower xlim: ').grid(row=0,column=4,padx=2,pady=2)
        self.low_xlim_entry = ttk.Entry(self.options_frame)
        ttk.Label(self.options_frame,text = 'Lower ylim: ').grid(row=0,column=8,padx=2,pady=2)
        self.low_ylim_entry = ttk.Entry(self.options_frame)
        self.low_xlim_entry.grid(row=0,column=5)
        self.low_ylim_entry.grid(row=0,column=9)

        ttk.Label(self.options_frame, text = 'Higher xlim: ').grid(row=0,column=6,padx=2,pady=2)
        self.high_xlim_entry = ttk.Entry(self.options_frame)
        ttk.Label(self.options_frame,text = 'Higher ylim: ').grid(row=0,column=10,padx=2,pady=2)
        self.high_ylim_entry = ttk.Entry(self.options_frame)
        self.high_xlim_entry.grid(row=0,column=7)
        self.high_ylim_entry.grid(row=0,column=11)

        '''ttk.Label(self.options_frame,text = 'Ideal X: ').grid(row=1,column=0,padx=2,pady=2)
        self.ideal_x_entry = ttk.Entry(self.options_frame)
        ttk.Label(self.options_frame, text = 'Ideal Y: ').grid(row=1,column=2,padx=2,pady=2)
        self.ideal_y_entry = ttk.Entry(self.options_frame)
        self.ideal_x_entry.grid(row=1,column=1,padx=2,pady=2)
        self.ideal_y_entry.grid(row=1,column=3,padx=2,pady=2)'''

        #buttons for graphs
        self.scatter_btn = ttk.Button(self.buttons_frame,text = 'Scatter Plot',
                           command = lambda : tooltip.Popgraph(self.data,
                                                                  self.tkvar1.get(),
                                                                  self.tkvar2.get(),
                                                                  'scatter',
                                                                  self.low_xlim_entry.get(),
                                                                  self.low_ylim_entry.get(),
                                                                  self.high_xlim_entry.get(),
                                                                  self.high_ylim_entry.get(),
                                                                  self.tkvar3.get()
                                                                  )
                                        )
        self.line_btn = ttk.Button(self.buttons_frame,text = 'Line Plot',
                                command = lambda: tooltip.Popgraph(self.data,
                                                                       self.tkvar1.get(),
                                                                       self.tkvar2.get(),
                                                                       'line',
                                                                       self.low_xlim_entry.get(),
                                                                       self.low_ylim_entry.get(),
                                                                       self.high_xlim_entry.get(),
                                                                       self.high_ylim_entry.get(),
                                                                       self.tkvar3.get()
                                                                       )
                                    )

        self.scatter_btn.grid(row=0,column=0,padx=2,pady=2)
        self.line_btn.grid(row=0,column=1,padx=2,pady=2)



        self.options_frame.pack(anchor=W,padx=10,pady=10)
        self.buttons_frame.pack(anchor=W,padx=10,pady=10)




    def clear(self):
            try:
                self.path_entry.delete(0,'end')
                self.options_frame.pack_forget()
                self.options_frame.destroy()
                self.buttons_frame.pack_forget()
                self.buttons_frame.destroy()
            except AttributeError: #incase user clicks clear before above frames are packed
                        pass

    def read_file(self,path):
        try:
            if '.csv' in path:
                data = pd.read_csv(path)
                return data
            elif '.xls' in path or '.xlsx' in path:
                data = pd.read_excel(path)
                return data
        except FileNotFoundError:
            messagebox.showerror(title = 'Error', message = 'Incorrect/Blank path!')


    def show_help(self,master):
        messagebox.showinfo(title = 'About', message = 'Contact sachin in case of queries or bugs')

def main():
    root = Tk()
    root.title('Viz Board')
    vizboard = Vizboard(root)
    root.mainloop()


if __name__ == '__main__':
    main()

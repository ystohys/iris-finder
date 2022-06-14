import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_utils import *


class App:
    
    def __init__(self, parent):
        self.data_obj = None
        self.tab_control = ttk.Notebook(parent)
        
        self.data_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.data_tab, text="Load Data")
        
        self.nb_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.nb_tab, text="Find Similar Flowers")
        self.tab_control.pack(expand=1, fill="both")
        
        ### Under Load Data tab
        
        # For data loading window
        self.load_frame = ttk.Frame(self.data_tab, 
                                    borderwidth=4,
                                    relief='ridge')
        self.load_frame.grid(column=0, row=0, sticky='ew')
        #self.data_tab.grid_columnconfigure(0,weight=1)
        
        self.drop_null = tk.BooleanVar()
        self.drop_dup = tk.BooleanVar()
        self.drop_out = tk.BooleanVar()
        self.path_lab = ttk.Label(self.load_frame, text='Path to CSV file:')
        self.path_name = ttk.Entry(self.load_frame)
        self.null_boo = tk.Checkbutton(self.load_frame, 
                                       text='Remove rows with missing data', 
                                       variable=self.drop_null)
        self.dup_boo = tk.Checkbutton(self.load_frame,
                                      text='Remove duplicate rows',
                                      variable=self.drop_dup)
        self.out_boo = tk.Checkbutton(self.load_frame, 
                                      text='Remove rows with outliers',
                                      variable=self.drop_out)
        self.path_lab.pack(anchor=tk.W)
        self.path_name.pack(anchor=tk.W)
    
        for i, checks in enumerate([self.null_boo, self.dup_boo, self.out_boo]):
            checks.pack(anchor=tk.W)
            
        self.load_but = tk.Button(self.load_frame, 
                                  height=5,
                                  width=30,
                                  text='Click here to load data', 
                                  command=lambda: [self.load_data_obj(self.path_name.get(),
                                                                     self.drop_dup.get(),
                                                                     self.drop_null.get(),
                                                                     self.drop_out.get()),
                                                   self.create_overview_plots(
                                                       self.dist_frame,
                                                       plot_func=self.plot_type.get())
                                                  ])
        self.load_but.pack(side=tk.BOTTOM)
        
        # For data distribution window
        self.dist_frame = ttk.Frame(self.data_tab, borderwidth=4, relief='ridge')
        self.dist_frame.grid(column=0, row=1, sticky='ew')
        self.dist_header = ttk.Label(self.dist_frame, text='Data Overview', 
                                     font='Helvetica 18 bold')
        self.dist_header.grid(column=0, row=0, columnspan=2)
        self.plot_type = tk.StringVar()
        self.dist_select = ttk.OptionMenu(self.dist_frame, 
                                          self.plot_type,
                                          "-Choose whether to stratify data for visualization-",
                                          *['Overall', 'Stratified'])
        self.dist_select.grid(column=0, row=1, columnspan=2)
        
        
        ### Under Find Similar Flowers Tab
        # Get new observation measurements
        self.input_frame = ttk.Frame(self.nb_tab,
                                     borderwidth=4,
                                     relief='ridge')
        self.input_frame.grid(column=0, row=0, columnspan=2, sticky='ew')
        self.sl_lab = ttk.Label(self.input_frame, text='Sepal Length:')
        self.sl_lab.pack(anchor=tk.W)
        self.sep_length = ttk.Entry(self.input_frame)
        self.sep_length.pack(anchor=tk.W)
        self.sw_lab = ttk.Label(self.input_frame, text='Sepal Width:')
        self.sw_lab.pack(anchor=tk.W)
        self.sep_width = ttk.Entry(self.input_frame)
        self.sep_width.pack(anchor=tk.W)
        self.pl_lab = ttk.Label(self.input_frame, text='Petal Length:')
        self.pl_lab.pack(anchor=tk.W)
        self.pet_length = ttk.Entry(self.input_frame)
        self.pet_length.pack(anchor=tk.W)
        self.pw_lab = ttk.Label(self.input_frame, text='Petal Width:')
        self.pw_lab.pack(anchor=tk.W)
        self.pet_width = ttk.Entry(self.input_frame)
        self.pet_width.pack(anchor=tk.W)
        self.new_obs = None
        self.tbl_width = None
        self.tbl_height = None
        
        self.nb_but = tk.Button(self.input_frame,
                                height=5,
                                width=30,
                                text='Click here to obtain data of similar flowers',
                                command=lambda: [
                                    self.load_inputs(),
                                    self.create_neighbor_plots(
                                        self.results_frame,
                                        self.new_obs
                                )])
        self.nb_but.pack(side=tk.BOTTOM)
        
        # Generating table and plot of neighbors and neighbor measurements
        self.results_frame = ttk.Frame(self.nb_tab,
                                       borderwidth=4,
                                       relief='ridge')
        self.results_frame.grid(column=0, row=1, columnspan=2, sticky='ew')
        self.res_header = ttk.Label(self.results_frame, 
                                    text='Data of 10 most similar flowers',
                                    font='Helvetica 18 bold')
        self.res_header.grid(column=0, row=0, columnspan=2)
        
        
    def load_data_obj(self, filepath, rm_dup, rm_null, rm_out):
        if rm_out:
            self.data_obj = IrisDataset(filepath, rm_dup, rm_null, rm_out, scale_mode='minmax')
        else:
            self.data_obj = IrisDataset(filepath, rm_dup, rm_null, rm_out)
            
    def load_inputs(self):
        self.new_obs = {'sepal_length': float(self.sep_length.get()),
                        'sepal_width': float(self.sep_width.get()),
                        'petal_length': float(self.pet_length.get()),
                        'petal_width': float(self.pet_width.get())}
        if self.tbl_width is None:
            self.tbl_width = int(self.nb_tab.winfo_width()/12)
        if self.tbl_height is None:
            self.tbl_height = int((self.nb_tab.winfo_height()-self.input_frame.winfo_height())/11)
            
    def create_overview_plots(self, parent, plot_func):
        if plot_func == 'Overall':
            fig1 = self.data_obj.plot_overall_boxplot(for_tk=True)
            fig2 = self.data_obj.plot_overall_vplot(for_tk=True)
        else:
            fig1 = self.data_obj.plot_stratified_boxplot(for_tk=True)
            fig2 = self.data_obj.plot_stratified_vplot(for_tk=True)
            
        canvas1 = FigureCanvasTkAgg(fig1, master=parent)
        canvas1.draw()
        canvas1.get_tk_widget().grid(column=0, row=2)
        canvas1.get_tk_widget().grid_columnconfigure(0, weight=1)
        
        canvas2 = FigureCanvasTkAgg(fig2, master=parent)
        canvas2.draw()
        canvas2.get_tk_widget().grid(column=1, row=2)
        canvas2.get_tk_widget().grid_columnconfigure(1, weight=1)
        
    def create_neighbor_plots(self, parent, obs):
        nb_df = self.data_obj.get_knn(obs).round(3)
        cols = list(nb_df.columns)
        style = ttk.Style(parent)
        style.configure('Treeview', rowheight=self.tbl_height, 
                        background='black',
                        fieldbackground='black',
                        foreground='white')
        tree = ttk.Treeview(parent, columns=cols, show='headings')
        for i in cols:
            tree.column(i, width=self.tbl_width, anchor="w")
            tree.heading(i, text=i)
        for index, row in nb_df.iterrows():
            tree.insert("",0,text=index,values=list(row))
        tree.grid(column=0, row=2)
        tree.grid_columnconfigure(0, weight=1)
        
        fig = self.data_obj.plot_neighbors(obs, for_tk=True)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().grid(column=1, row=2)
        canvas.get_tk_widget().grid_columnconfigure(1, weight=1)
        
        
def on_close():
    plt.close("all")
    root.destroy()
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('IrisFinder')
    App(root)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

from myimports import (
    sys, tk, ttk, filedialog, mysql, pd,
    create_engine, text, Integer, Text, String, DateTime, Boolean,
    sns, plt, np, Image, ImageTk,
    large_font, medium_font, small_bold, server_details, sqlalc_eng, dfi, io
)

from currentdf import DF

class DataFrameToolbar:
            
    def on_column_combobox_select(self, event):
        selected_column = self.column_combobox.get()
    
        if selected_column:
            # Get the data type of a specific column
            column_type = DF.current_df[selected_column].dtype
            self.print_msg("DataType: "+str(column_type), "green")
            
                    
    
    def convert_dtype(self):
        selected_column = self.column_combobox.get()
        
        selected_dtype = self.dtype_combobox.get()
        
        if selected_column and selected_dtype:
            
            try:
                # Convert selected to selected data type
                DF.current_df[selected_column] = DF.current_df[selected_column].astype(selected_dtype)
                column_type = DF.current_df[selected_column].dtype
                self.print_msg("DataType: "+str(column_type), "darkorange")
            
            except KeyError:
                self.print_msg("Invalid column selection", "red")
            except TypeError:
                self.print_msg("Conversion failed", "red")
            except ValueError:
                self.print_msg("Conversion failed", "red")
        else:
            self.print_msg("Select DType!", "red")
            
            
    def gen_plt(self):
        selected_plt = self.plt_combobox.get()
        
        if selected_plt:
            if selected_plt != 'scatterplot':
                x_axis = self.x_combobox.get()
                y_axis = self.y_combobox.get()

                if x_axis and y_axis:
                    plt.figure(figsize=(8,8))

                    if selected_plt == 'regplot':
                        self.hue_combobox.set("")
                        try:
                            regplot = sns.regplot(data=DF.current_df, x=x_axis, y=y_axis)
                            regplot.figure.savefig(self.plt_filename)
                        except TypeError as e:
                                self.print_msg(e, "red")
                                print("TypeError occurred:", e)
                                return

                    elif selected_plt == 'lmplot':
                        hue = self.hue_combobox.get()
                        if hue:
                            try:
                                lmplot = sns.lmplot(data=DF.current_df, x=x_axis, y=y_axis, hue=hue)
                            except TypeError as e:
                                self.print_msg(e, "red")
                                print("TypeError occurred:", e)
                                return
                            
                        else:
                            try:
                                lmplot = sns.lmplot(data=DF.current_df, x=x_axis, y=y_axis)
                            except TypeError as e:
                                self.print_msg(e, "red")
                                print("TypeError occurred:", e)
                                return
                            
                        lmplot.savefig(self.plt_filename, dpi=120)
                        self.print_msg("Lmplot Successful.", "green")
                          

                    elif selected_plt == 'jointplot':
                        hue = self.hue_combobox.get()

                        if hue:
                            try:
                                jointplot = sns.jointplot(data=DF.current_df, x=x_axis, y=y_axis, hue=hue)
                                jointplot.plot_joint(sns.kdeplot, hue=hue, warn_singular=False)
                            except TypeError as e:
                                self.print_msg(e, "red")
                                print("TypeError occurred:", e)
                                return

                        else:
                            try:
                                jointplot = sns.jointplot(data=DF.current_df, x=x_axis, y=y_axis, kind="reg")
                            except TypeError as e:
                                self.print_msg(e, "red")
                                print("TypeError occurred:", e)
                                return
                            
                        jointplot.savefig(self.plt_filename, dpi=100)
                        self.print_msg("Jointplot Successful.", "green")
                            
                else:
                    self.print_msg("X and Y needed for plot!", "red")
                    return
                            

            else:
                hue = self.hue_combobox.get()
                if hue:
                    scatterplot = sns.pairplot(DF.current_df, kind= 'scatter', hue=hue)
                    self.x_combobox.set("")
                    self.y_combobox.set("")

                else:
                    scatterplot = sns.pairplot(DF.current_df, kind= 'scatter')
                    self.x_combobox.set("")
                    self.y_combobox.set("")
                    
                # save plot to jpg file
                scatterplot.savefig(self.plt_filename)
                self.print_msg("Scatterplot Successful.", "green")
                
            self.view_window.change_image(self.plt_filename)
  
        else:
            self.print_msg("No Plot Selected!", "red") 
            
    def view_df_info(self):
        
        # Capture the output of df.info()
        buffer = io.StringIO()
        DF.current_df.info(buf=buffer)

        # Create a figure and axes
        fig, ax = plt.subplots(figsize=(2, 1))

        # Set the axes properties
        ax.axis('off')

        # Plot the captured output as text
        ax.text(0, 1, buffer.getvalue(), fontsize=4, va='top')

        # Save the figure as a JPEG image
        plt.savefig('dtypes.jpg', bbox_inches='tight', dpi=300)
        
        dfi.export(DF.current_df.head(10), 'dfhead.jpg', dpi=100)
        
        # Open the image
        image1 = Image.open('dtypes.jpg')
        # Get the size of the image
        width1, height1 = image1.size
        
        # Open the image
        image2 = Image.open('dfhead.jpg')
        # Get the size of the image
        width2, height2 = image2.size
        
        if width1 > width2:
            # Create a new image with the combined size
            combined_image = Image.new("RGB", (width1, height1+height2), (255, 255, 255))
        else:
            # Create a new image with the combined size
            combined_image = Image.new("RGB", (width2, height1+height2), (255, 255, 255))

        # Paste the first image on the left side
        combined_image.paste(image1, (0, 0))

        # Paste the second image on the right side
        combined_image.paste(image2, (0, height1))

        # Save the combined image
        combined_image.save('dataframe.jpg')
        
        self.view_window.change_image('dataframe.jpg')
        
    def print_msg(self, msg, color):
        self.dtype_label.config(text=msg, foreground=color, font=small_bold)
    
    def __init__(self, frame, view_window):
        self.home_frame = frame
        self.view_window = view_window
        self.current_dataframe = pd.DataFrame()
        self.selected_table = ""
        self.plt_filename = "plt.jpg"
        self.dtypes = ['int', 'float', 'bool', 'category', 'datetime64[ns]', 'timedelta64[ns]']
        self.plt_types = ['regplot', 'lmplot', 'jointplot', 'scatterplot']
        
        # Create tool bar frame
        self.dataframe_tool_bar = tk.Frame(self.home_frame, width=180, height=185, relief='ridge')
        self.dataframe_tool_bar.grid(row=1, column=1, padx=3, pady=3)

        # Create a label for the table selection
        self.table_label = ttk.Label(self.dataframe_tool_bar, text="DataFrame Toolbar", font=large_font, relief='raised')
        self.table_label.grid(row=1, column=0, columnspan=2, pady=3, sticky="s")
        
        # Create a label for the table selection
        self.which_table_label = ttk.Label(self.dataframe_tool_bar, text="Table: NONE", foreground="green", font=small_bold, justify='center', wraplength=180)
        self.which_table_label.grid(row=2, column=0, columnspan=2)

        # Create a label for the table creation section
        self.create_label = ttk.Label(self.dataframe_tool_bar, text="Convert Data Types", font=medium_font)
        self.create_label.grid(row=4, column=0, columnspan=2)
        
        # Create a label for the table selection
        self.table_label = ttk.Label(self.dataframe_tool_bar, text="Column:")
        self.table_label.grid(row=5, column=0, sticky='e')
        
        # Create a combobox for table selection
        self.column_combobox = ttk.Combobox(self.dataframe_tool_bar, width=13)
        self.column_combobox.grid(row=5, column=1, padx=2)
        self.column_combobox.bind("<<ComboboxSelected>>", self.on_column_combobox_select)
        
        # Create a scrollbar
        #self.col_listbox_scrollbar = ttk.Scrollbar(self.dataframe_tool_bar)
        #self.col_listbox_scrollbar.grid(row=6, column=1, sticky='ns')

        # Create a Listbox widget
        #self.column_listbox = tk.Listbox(self.dataframe_tool_bar, height=2, width=22, yscrollcommand=self.col_listbox_scrollbar.set, selectmode=tk.SINGLE)
        #self.column_listbox.grid(row=6, column=0, padx=2, sticky='nsew')
        #self.column_listbox.bind("<<ListboxSelect>>", self.on_column_combobox_select)

        # Configure the scrollbar to scroll the Listbox
        #self.col_listbox_scrollbar.config(command=self.column_listbox.yview)
        
        # Create a label for the datatype selection
        self.dtype_label = ttk.Label(self.dataframe_tool_bar, text="DataType:")
        self.dtype_label.grid(row=7, column=0, sticky='e')

        # Create a combobox for table selection
        self.dtype_combobox = ttk.Combobox(self.dataframe_tool_bar, width=13)
        self.dtype_combobox.grid(row=7, column=1, padx=2)
        
        # Populate the table combobox with the table names
        self.dtype_combobox["values"] = self.dtypes
        self.dtype_combobox.set("")  # Clear the selection

        
        # Create a button to create the table
        self.conv_dtype_button = ttk.Button(self.dataframe_tool_bar, text="Convert DType", command=self.convert_dtype)
        self.conv_dtype_button.grid(row=9, column=0, columnspan=2, padx=3, sticky="w")
        
        # Create a button to create the table
        self.df_info_button = ttk.Button(self.dataframe_tool_bar, text="Info", command=self.view_df_info)
        self.df_info_button.grid(row=9, column=1, padx=3, sticky="e")
        self.df_info_button.configure(width=3)
        
        # Create a label to display success message
        self.dtype_label = ttk.Label(self.dataframe_tool_bar, justify='center', wraplength=180)
        self.dtype_label.grid(row=10, column=0, columnspan=3, pady=3, sticky="n")
        
        

        # Create a label for the table creation section
        self.delete_label = ttk.Label(self.dataframe_tool_bar, text="Visualize Data", font=medium_font)
        self.delete_label.grid(row=12, column=0, columnspan=2)
        
        # Create a label for the datatype selection
        self.x_label = ttk.Label(self.dataframe_tool_bar, text="X Axis:")
        self.x_label.grid(row=13, column=0, sticky='e')
        
        # Create a combobox for table selection
        self.x_combobox = ttk.Combobox(self.dataframe_tool_bar, width=13)
        self.x_combobox.grid(row=13, column=1, padx=2)
        
        # Create a label for the datatype selection
        self.y_label = ttk.Label(self.dataframe_tool_bar, text="Y Axis:")
        self.y_label.grid(row=14, column=0, sticky='e')
        
        # Create a combobox for table selection
        self.y_combobox = ttk.Combobox(self.dataframe_tool_bar, width=13)
        self.y_combobox.grid(row=14, column=1, padx=2)
        
        # Create a label for the datatype selection
        self.hue_label = ttk.Label(self.dataframe_tool_bar, text="Hue:")
        self.hue_label.grid(row=15, column=0, sticky='e')
        
        # Create a combobox for table selection
        self.hue_combobox = ttk.Combobox(self.dataframe_tool_bar, width=13)
        self.hue_combobox.grid(row=15, column=1, padx=2)
        
        # Create a label for the datatype selection
        self.plt_label = ttk.Label(self.dataframe_tool_bar, text="Plot Type:")
        self.plt_label.grid(row=16, column=0, sticky='e')
        
        # Create a combobox for table selection
        self.plt_combobox = ttk.Combobox(self.dataframe_tool_bar, width=13)
        self.plt_combobox.grid(row=16, column=1, padx=2)
        
        
        # Populate the table combobox with the table names
        self.plt_combobox["values"] = self.plt_types
        self.plt_combobox.set("")  # Clear the selection
        
        # Create a button to create the table
        self.gen_plt_button = ttk.Button(self.dataframe_tool_bar, text="Generate Plot", command=self.gen_plt)
        self.gen_plt_button.grid(row=17, column=0, columnspan=2, sticky="n")

        

        self.dataframe_tool_bar.rowconfigure(3, minsize=3)
        #self.dataframe_tool_bar.rowconfigure(11, minsize=10)
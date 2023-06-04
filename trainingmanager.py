from myimports import (
    sys, tk, ttk, filedialog, mysql, pd,
    create_engine, text, Integer, Text, String, DateTime, Boolean,
    sns, plt, Image, ImageTk,
    large_font, medium_font, small_bold, server_details, sqlalc_eng
)

from currentdf import DF


class TrainingManager:
    
    def on_combobox_select(self, event):
        selected_table = self.table_combobox.get()
        if selected_table:
        
            # Connect to the MariaDB server
            connection = mysql.connect(**server_details)

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Execute a query to fetch the columns of the selected table
            cursor.execute(f"SHOW COLUMNS FROM `{selected_table}`")

            # Fetch all the column names
            columns = cursor.fetchall()
        
            # Fetch all the data to create a dataframe for visualizing in pairplot
            #query = "SELECT * FROM `{selected_table}`"
            #cursor.execute(f"SELECT * FROM `{selected_table}`")
            #rows = cursor.fetchall()
        
            #column_names = []  # Create an empty list

            # Populate the column_listbox with the column names
            self.ind_column_listbox.delete(0, tk.END)  # Clear previous items
            self.dep_column_listbox.delete(0, tk.END)  # Clear previous items
            self.xcolumn_listbox.delete(0, tk.END)  # Clear previous items
            self.pred_label.config(text="")
            
            self.dataframe_toolbar.column_combobox["values"] = [column[0] for column in columns]
            self.dataframe_toolbar.column_combobox.set("")
            #self.dataframe_toolbar.column_listbox.delete(0, tk.END) # Clear previous items in dataframe toolbar column listbox
            self.dataframe_toolbar.dtype_combobox.set("") # Clear previous datatype selection
            
            self.dataframe_toolbar.x_combobox["values"] = ["", *[column[0] for column in columns]]
            self.dataframe_toolbar.x_combobox.set("")
            
            self.dataframe_toolbar.y_combobox["values"] = ["", *[column[0] for column in columns]]
            self.dataframe_toolbar.y_combobox.set("")
            
            self.dataframe_toolbar.hue_combobox["values"] = ["", *[column[0] for column in columns]]
            self.dataframe_toolbar.hue_combobox.set("")
            
            for column in columns:
                self.ind_column_listbox.insert(tk.END, column[0])
                self.dep_column_listbox.insert(tk.END, column[0])
                #self.dataframe_toolbar.column_listbox.insert(tk.END, column[0])
                #column_names.append(column[0])
            
            #df = pd.DataFrame(rows, columns=column_names)
        
            query = f"SELECT * FROM `{selected_table}`"
        
            # Create SQLAlchemy engine
            engine = create_engine(sqlalc_eng)

            # Read the table data into a Pandas DataFrame
            DF.current_df = pd.read_sql_query(sql=text(query), con=engine.connect())
        
            # Close the SQLAlchemy engine
            engine.dispose()
            
        
            DF.current_df.info()
        
            self.dataframe_toolbar.view_df_info()
            # Generate a pairplot to quickly see how varaiables relate to one another
            #pairplot = sns.pairplot(DF.current_df, kind= 'scatter')
            
            # Replace 'filename' with the desired name of your output file
            #pairplot.savefig(self.plt_filename)
        
            #self.view_window.change_image(self.plt_filename)
        
            
            self.dataframe_toolbar.which_table_label.config(text=f"Table: '{selected_table}'")
            self.dataframe_toolbar.dtype_label.config(text="")
       
           
            # Close the cursor and connection
            cursor.close()
            connection.close()
   
            
    def move_items(self, from_box, to_box, to_single_item, from_single_item):
        print("Button pushed")
        if from_single_item:
            selected_item = from_box["text"]
            if selected_item:
                to_box.insert(tk.END, selected_item)
                self.ind_column_listbox.insert(tk.END, selected_item)
                from_box.config(text="")
            
        else:      
            if from_box.curselection():
                selected_item = from_box.get(from_box.curselection())

                if selected_item:

                    if to_single_item:
                        if selected_item:
                            to_box_value = to_box["text"]
                            if to_box_value:
                                print("Column already selected")
                            else:
                                to_box.config(text=selected_item)
                                self.ind_column_listbox.delete(from_box.curselection())
                                from_box.delete(from_box.curselection())
                                

                    else:
                        if from_box == self.ind_column_listbox:
                            to_box.insert(tk.END, selected_item)
                            self.dep_column_listbox.delete(from_box.curselection())
                            from_box.delete(from_box.curselection())
                            
                        else:
                            to_box.insert(tk.END, selected_item)
                            self.dep_column_listbox.insert(tk.END, selected_item)
                            from_box.delete(from_box.curselection())
                          
            else:
                print("No Column selected")

    def on_alg_combobox_select(self, event):
        selected_alg = self.algorithm_combobox.get()
        if selected_alg:
            # Populate the algorithms combobox with the algorithm names
            self.method_combobox["values"] = self.algorithm_methods[selected_alg]
            self.method_combobox.set("")  # Clear the selection
            if selected_alg == "Clustering":
                # Enable cluster GUI elements
                self.cluster_label.config(state="normal")
                self.cluster_slider.config(state="normal")
            else:
                # Disable cluster GUI elements
                self.cluster_label.config(state="disabled")
                self.cluster_slider.config(state="disabled")
                    
                    
    def handle_slider(self, event):
        value = int(self.cluster_slider.get())
        self.cluster_slider.set(value)
        self.cluster_label.config(text="Clusters: "+str(value))  
        
    
    def start_algorithm(self):
        selected_table = table_combobox.get()
        selected_columns = column_combobox.get()
        # Add code to start the machine learning algorithm with the selected table and columns

    
    def __init__(self, frame, view_window, dataframe_toolbar):
        self.home_frame = frame
        self.view_window = view_window
        self.current_dataframe = pd.DataFrame()
        self.dataframe_toolbar = dataframe_toolbar
        self.plt_filename = "plt.jpg"
        self.algorithms = ['Linear Reg', 'Classification', 'Clustering']
        self.algorithm_methods = {
            "Linear Reg": [],
            "Classification": ["KNeigbors", "Decision Tree"],
            "Clustering": ["KMeans", "Gaussian Mixture", "Spectral Clustering"]
        }
        self.scale_types = ["", "Standardize", "Normalize"]
        self.test_sizes = [10, 20, 30]

        # Create left and right frames
        self.training_manager = tk.Frame(self.home_frame, width=180, height=185, bg='Purple2', relief='ridge')
        self.training_manager.grid(row=0, column=0, columnspan=2, padx=3, pady=3)
    
        # Create a label for the table selection
        self.table_label = ttk.Label(self.training_manager, text="Training Manager", font=large_font, relief='raised')
        self.table_label.grid(row=0, column=0, columnspan=10)
    
        # Create a label for the table selection
        self.table_label = ttk.Label(self.training_manager, text="Select a table:")
        self.table_label.grid(row=2, column=0, columnspan=5)

        # Create a combobox for table selection
        self.table_combobox = ttk.Combobox(self.training_manager)
        self.table_combobox.grid(row=3, column=0, columnspan=5)
        # Bind the function to the combobox selection event
        self.table_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # Create a label for the column selection
        self.ind_column_label = ttk.Label(self.training_manager, text="Independent Variable(s):")
        self.ind_column_label.grid(row=5, column=0, columnspan=2)

        # Create a scrollbar
        self.ind_scrollbar = ttk.Scrollbar(self.training_manager)
        self.ind_scrollbar.grid(row=6, column=1, rowspan=4, sticky='ns')

        # Create a Listbox widget
        self.ind_column_listbox = tk.Listbox(self.training_manager, height=4, width=15, yscrollcommand=self.ind_scrollbar.set)
        self.ind_column_listbox.grid(row=6, column=0, rowspan=4, sticky='nsew')

        # Configure the scrollbar to scroll the Listbox
        self.ind_scrollbar.config(command=self.ind_column_listbox.yview)
        
        # Create a label for the column selection
        self.xcolumn_label = ttk.Label(self.training_manager, text="Feature(s):")
        self.xcolumn_label.grid(row=5, column=4, columnspan=2)

        # Create a scrollbar
        self.x_scrollbar = ttk.Scrollbar(self.training_manager)
        self.x_scrollbar.grid(row=6, column=5, rowspan=4, sticky='ns')

        # Create a Listbox widget
        self.xcolumn_listbox = tk.Listbox(self.training_manager, height=4, width=15, yscrollcommand=self.x_scrollbar.set)
        self.xcolumn_listbox.grid(row=6, column=4, rowspan=4, sticky='nsew')

        # Configure the scrollbar to scroll the Listbox
        self.x_scrollbar.config(command=self.xcolumn_listbox.yview)
        
        # Create a button to move selected items from the independent column Listbox to the dependent column Listbox
        self.xmove_button = ttk.Button(self.training_manager, text="-->", command=lambda: self.move_items(self.ind_column_listbox, self.xcolumn_listbox, False, False))
        self.xmove_button.grid(row=7, column=3, padx=3)
        self.xmove_button.configure(width=2)

        # Create a button to move selected items from the dependent column Listbox to the independent column Listbox
        self.xmove_back_button = ttk.Button(self.training_manager, text="<--", command=lambda: self.move_items(self.xcolumn_listbox, self.ind_column_listbox, False, False))
        self.xmove_back_button.grid(row=8, column=3, padx=3)
        self.xmove_back_button.configure(width=2)
        
        
        # Create a label for the column selection
        self.dep_column_label = ttk.Label(self.training_manager, text="Dependent Variable:")
        self.dep_column_label.grid(row=10, column=0, columnspan=2)

        # Create a scrollbar
        self.dep_scrollbar = ttk.Scrollbar(self.training_manager)
        self.dep_scrollbar.grid(row=11, column=1, rowspan=4, sticky='ns')

        # Create a Listbox widget
        self.dep_column_listbox = tk.Listbox(self.training_manager, height=4, width=15, yscrollcommand=self.dep_scrollbar.set)
        self.dep_column_listbox.grid(row=11, column=0, rowspan=4, sticky='nsew')

        # Configure the scrollbar to scroll the Listbox
        self.dep_scrollbar.config(command=self.dep_column_listbox.yview)
        
        # Create a label for the column selection
        self.ycolumn_label = ttk.Label(self.training_manager, text="Predict:")
        self.ycolumn_label.grid(row=11, column=4, columnspan=2, rowspan=2, pady=1, sticky='s')
        
        # Create a label for the column selection
        self.pred_label = ttk.Label(self.training_manager, width=15)
        self.pred_label.grid(row=13, column=4, columnspan=2, rowspan=2, pady=1, sticky='n')
        
        # Create a button to move selected items from the independent column Listbox to the dependent column Listbox
        self.ymove_button = ttk.Button(self.training_manager, text="-->", command=lambda: self.move_items(self.dep_column_listbox, self.pred_label, True, False))
        self.ymove_button.grid(row=12, column=3, padx=3)
        self.ymove_button.configure(width=2)

        # Create a button to move selected items from the dependent column Listbox to the independent column Listbox
        self.ymove_back_button = ttk.Button(self.training_manager, text="<--", command=lambda: self.move_items(self.pred_label, self.dep_column_listbox, False, True))
        self.ymove_back_button.grid(row=13, column=3, padx=3)
        self.ymove_back_button.configure(width=2)
        
        # Create a label for the table selection
        self.algorithm_label = ttk.Label(self.training_manager, text="Algorithm:")
        self.algorithm_label.grid(row=2, column=6, columnspan=2, pady=2, sticky="s")

        # Create a combobox for table selection
        self.algorithm_combobox = ttk.Combobox(self.training_manager, width=13)
        self.algorithm_combobox.grid(row=3, column=6, columnspan=2, padx=3)
        # Bind the function to the combobox selection event
        self.algorithm_combobox.bind("<<ComboboxSelected>>", self.on_alg_combobox_select)
        
        # Populate the algorithms combobox with the algorithm names
        self.algorithm_combobox["values"] = self.algorithms
        self.algorithm_combobox.set("")  # Clear the selection
        
        # Create a label for the table selection
        self.method_label = ttk.Label(self.training_manager, text="Method:")
        self.method_label.grid(row=5, column=6, columnspan=2, pady=2, sticky="s")

        # Create a combobox for table selection
        self.method_combobox = ttk.Combobox(self.training_manager, width=13)
        self.method_combobox.grid(row=6, column=6, columnspan=2, padx=3)
        
        # Create a label for the table selection
        self.scale_label = ttk.Label(self.training_manager, text="Scaling:")
        self.scale_label.grid(row=7, column=6, columnspan=2, pady=2, sticky="s")

        # Create a combobox for table selection
        self.scale_combobox = ttk.Combobox(self.training_manager, width=13)
        self.scale_combobox.grid(row=8, column=6, columnspan=2, padx=3, sticky="n")
        # Populate the algorithms combobox with the algorithm names
        self.scale_combobox["values"] = self.scale_types
        self.scale_combobox.set("")  # Clear the selection
        
        # Create a label for the table selection
        self.test_size_label = ttk.Label(self.training_manager, text="Test Size:")
        self.test_size_label.grid(row=9, column=6, sticky="e")

        # Create a combobox for table selection
        self.test_size_combobox = ttk.Combobox(self.training_manager, width=5)
        self.test_size_combobox.grid(row=9, column=7, padx=1, pady=2)
        # Populate the algorithms combobox with the algorithm names
        self.test_size_combobox["values"] = self.test_sizes
        self.test_size_combobox.set(20)  # Clear the selection
        
        # Create a label for the table selection
        self.cluster_label = ttk.Label(self.training_manager, text="Clusters: 1")
        self.cluster_label.grid(row=10, column=6, columnspan=2, pady=2, sticky="s")
        
        self.cluster_slider = ttk.Scale(self.training_manager, from_=1, to=100, orient="horizontal", length=140)
        self.cluster_slider.grid(row=11, column=6, columnspan=2,)
        self.cluster_slider.bind("<B1-Motion>", self.handle_slider)
        self.cluster_slider.set(1)
                                  
        # Disable cluster GUI elements by default
        self.cluster_label.config(state="disabled")
        self.cluster_slider.config(state="disabled")

        
        self.training_manager.rowconfigure(1, minsize=7)
        self.training_manager.rowconfigure(4, minsize=7)
        self.training_manager.rowconfigure(14, minsize=25)


        # Create a combobox for column selection
        #column_combobox = ttk.Combobox(root)
        #column_combobox.grid(row=5, column=3, columnspan=2)
    
        
        # Create a button to start the algorithm
        self.start_button = ttk.Button(self.training_manager, text="Train Model", command=self.start_algorithm)
        self.start_button.grid(row=12, column=6, columnspan=2, rowspan=3)
    
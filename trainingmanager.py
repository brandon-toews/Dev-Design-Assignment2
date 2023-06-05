from myimports import (
    sys, tk, ttk, filedialog, mysql, pd,
    create_engine, text, Integer, Text, String, DateTime, Boolean,
    sns, plt, Image, ImageTk,
    large_font, medium_font, small_bold, server_details, sqlalc_eng
)

from currentdf import DF
import algorithms as ml


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

            # Populate various comboboxes and listboxes based on table selection
            self.ind_column_listbox.delete(0, tk.END)  # Clear previous items
            self.dep_column_listbox.delete(0, tk.END)  # Clear previous items
            self.xcolumn_listbox.delete(0, tk.END)  # Clear previous items
            self.pred_label.config(text="")
            
            self.dataframe_toolbar.column_combobox["values"] = [column[0] for column in columns]
            self.dataframe_toolbar.column_combobox.set("")
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
                
            #query for SQLAlchemy to pull data from mariadb server
            query = f"SELECT * FROM `{selected_table}`"
        
            # Create SQLAlchemy engine
            engine = create_engine(sqlalc_eng)

            # Read the table data into a Pandas DataFrame
            DF.current_df = pd.read_sql_query(sql=text(query), con=engine.connect())
        
            # Close the SQLAlchemy engine
            engine.dispose()

            #display some info to useron selected datset
            self.dataframe_toolbar.view_df_info()
            
            #Confirm to user what table is selected
            self.dataframe_toolbar.which_table_label.config(text=f"Table: '{selected_table}'")
            self.dataframe_toolbar.dtype_label.config(text="")
       
           
            # Close the cursor and connection
            cursor.close()
            connection.close()
   
    #function to move column selections to indicate to user wha they have selected       
    def move_items(self, from_box, to_box, to_single_item, from_single_item):
        if from_single_item:
            selected_item = from_box["text"]
            if selected_item:
                to_box.insert(tk.END, selected_item)
                self.ind_column_listbox.insert(tk.END, selected_item)
                from_box.config(text="")
                self.print_msg("Choice successful.", "green")
            
        else:      
            if from_box.curselection():
                selected_item = from_box.get(from_box.curselection())

                if selected_item:

                    if to_single_item:
                        if selected_item:
                            to_box_value = to_box["text"]
                            if to_box_value:
                                self.print_msg("Predict column already selected!", "red")
                            else:
                                to_box.config(text=selected_item)
                                self.ind_column_listbox.delete(from_box.curselection())
                                from_box.delete(from_box.curselection())
                                self.print_msg("Choice successful.", "green")

                    else:
                        if from_box == self.ind_column_listbox:
                            to_box.insert(tk.END, selected_item)
                            self.dep_column_listbox.delete(from_box.curselection())
                            from_box.delete(from_box.curselection())
                            self.print_msg("Choice successful.", "green")
                            
                        else:
                            to_box.insert(tk.END, selected_item)
                            self.dep_column_listbox.insert(tk.END, selected_item)
                            from_box.delete(from_box.curselection())
                            self.print_msg("Choice successful.", "green")
                          
            else:
                self.print_msg("No Column selected!", "red")

    def on_alg_combobox_select(self, event):
        selected_alg = self.algorithm_combobox.get()
        if selected_alg:
            # Populate the algorithms combobox with the algorithm names
            self.method_combobox["values"] = self.algorithm_methods[selected_alg]
            #If algorithm has method options enable GUI elements to select them
            if self.method_combobox["values"]:
                self.method_combobox.config(state="normal")
                self.method_combobox.current(0) # Select first element in combobox
                self.method_label.config(state="normal")
            #If algorithm doesn't have method options disable GUI elements so user knows there aren't any
            else:
                self.method_combobox.set("")
                self.method_combobox.config(state="disabled")
                self.method_label.config(state="disabled")
                
            if selected_alg == "Clustering":
                #If column is selected for prediction clear selection for clustering
                self.move_items(self.pred_label, self.dep_column_listbox, False, True)
                # disable normal GUI elements
                self.ycolumn_label.config(state="disabled")
                self.pred_label.config(state="disabled")
                self.test_size_label.config(state="disabled")
                self.test_size_combobox.config(state="disabled")
                # Enable cluster GUI elements
                self.cluster_label.config(state="normal")
                self.cluster_slider.config(state="normal")
            else:
                # Disable cluster GUI elements
                self.cluster_label.config(state="disabled")
                self.cluster_slider.config(state="disabled")
                # enable normal GUI elements
                self.ycolumn_label.config(state="normal")
                self.pred_label.config(state="normal")
                self.test_size_label.config(state="normal")
                self.test_size_combobox.config(state="normal")
                    
    #function to handle cluster slider movements               
    def handle_slider(self, event):
        value = int(self.cluster_slider.get())
        self.cluster_slider.set(value)
        self.cluster_label.config(text="Clusters: "+str(value))  
        
    
    def train_model(self):
        #Get user selections
        x_columns = list(self.xcolumn_listbox.get(0, tk.END))
        y_column = self.pred_label["text"]
        algorithm_selection = self.algorithm_combobox.get()
        method_selection = self.method_combobox.get()
        scale_selection = self.scale_combobox.get()
        test_size = int(self.test_size_combobox.get())
        
        # Drop rows with NaN values
        df_cleaned = DF.current_df.dropna()
        
        if x_columns and y_column:              
            if algorithm_selection == "Linear Reg":
                #Grab the x values from the current dataframe using the columns selected
                x_values = df_cleaned.loc[:, x_columns].values
                #Grab the y value from the current dataframe using the columns selected
                y_value = df_cleaned.loc[:, y_column].values
                
                try:
                    #Train model and store jpg of the results
                    lin_reg_results = ml.myLinRegModel(x_values, y_value, scale_selection, test_size)
                #Display errors to user if there are any
                except TypeError as e:
                    self.print_msg(e, "red")
                    print("TypeError occurred:", e)
                    return
                except ValueError as e:
                    self.print_msg(e, "red")
                    print("ValueError occurred:", e)
                    return
                except IndexError as e:
                    self.print_msg(e, "red")
                    print("ValueError occurred:", e)
                    return
                #Display results in view window
                self.view_window.change_image(lin_reg_results)
                #Confirm to user model training was successful
                self.print_msg("Linear Regression model training successful.", "green")
                
            elif algorithm_selection == "Classification":
                #Grab the x values from the current dataframe using the columns selected
                x_values = df_cleaned[x_columns].values
                #Grab the y value from the current dataframe using the columns selected
                y_value = df_cleaned[y_column]
                
                try:
                    #Train model and store jpg of the results
                    class_results = ml.myClassModel(x_values, y_value, scale_selection, method_selection, test_size)
                #Display errors to user if there are any
                except TypeError as e:
                    self.print_msg(e, "red")
                    print("TypeError occurred:", e)
                    return
                except ValueError as e:
                    self.print_msg(e, "red")
                    print("ValueError occurred:", e)
                    return
                except IndexError as e:
                    self.print_msg(e, "red")
                    print("ValueError occurred:", e)
                    return
                #Display results in view window
                self.view_window.change_image(class_results)
                #Confirm to user model training was successful
                self.print_msg("Classification model training successful.", "green")
                
                
        elif algorithm_selection == "Clustering":
            if len(x_columns) > 1:
                #Grab the x values from the current dataframe using the columns selected
                x_values = df_cleaned[x_columns]
                #Grab num clusters from slider
                num_clusters = int(self.cluster_slider.get())
                try:
                    #Train model and store jpg of the results
                    cluster_results = ml.myClusterModel(x_values, scale_selection, method_selection, num_clusters)
                #Display errors to user if there are any
                except TypeError as e:
                    self.print_msg(e, "red")
                    print("TypeError occurred:", e)
                    return
                except ValueError as e:
                    self.print_msg(e, "red")
                    print("ValueError occurred:", e)
                    return
                except IndexError as e:
                    self.print_msg(e, "red")
                    print("ValueError occurred:", e)
                    return
                #Display results in view window
                self.view_window.change_image(cluster_results)
                #Confirm to user model training was successful
                self.print_msg("Cluster model training successful.", "green")
            elif len(x_columns) == 1:
                #Tell user to select features
                self.print_msg("Select one more feature!", "red")
            else:
                #Tell user to select features
                self.print_msg("Select at least two features!", "red")
            
        else:
            #tell user to select features and predict values
            self.print_msg("Select feature(s) and predict!", "red")
        
    def print_msg(self, msg, color):
        #Display message to user
        self.success_label.config(text=msg, foreground=color, font=small_bold)
    
    def __init__(self, frame, view_window, dataframe_toolbar):
        #initialize variables for setup
        self.home_frame = frame
        self.view_window = view_window
        self.current_dataframe = pd.DataFrame()
        self.dataframe_toolbar = dataframe_toolbar
        self.plt_filename = "plt.jpg"
        self.algorithms = ['Linear Reg', 'Classification', 'Clustering']
        self.algorithm_methods = {
            "Linear Reg": [],
            "Classification": ["KNeighbors", "Decision Tree"],
            "Clustering": ["KMeans", "Gaussian Mixture", "Spectral Clustering"]
        }
        self.scale_types = ["", "Standardize", "Normalize"]
        self.test_sizes = [10, 20, 30]

        # Create training manager toolbar
        self.training_manager = tk.Frame(self.home_frame, width=180, height=185, bg='plum4', relief='ridge')
        self.training_manager.grid(row=0, column=0, columnspan=2, padx=3, pady=3)
    
        # Create a label for toolbar
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

        # Create a label for independent column Listbox
        self.ind_column_label = ttk.Label(self.training_manager, text="Independent Variable(s):")
        self.ind_column_label.grid(row=5, column=0, columnspan=2)

        # Create a scrollbar for independent column Listbox
        self.ind_scrollbar = ttk.Scrollbar(self.training_manager)
        self.ind_scrollbar.grid(row=6, column=1, rowspan=4, sticky='ns')

        # Create an independent column Listbox
        self.ind_column_listbox = tk.Listbox(self.training_manager, height=4, width=15, yscrollcommand=self.ind_scrollbar.set)
        self.ind_column_listbox.grid(row=6, column=0, rowspan=4, sticky='nsew')

        # Configure the scrollbar to scroll independent column Listbox
        self.ind_scrollbar.config(command=self.ind_column_listbox.yview)
        
        # Create a label for x column Listbox
        self.xcolumn_label = ttk.Label(self.training_manager, text="Feature(s):")
        self.xcolumn_label.grid(row=5, column=4, columnspan=2)

        # Create a scrollbar for x column Listbox
        self.x_scrollbar = ttk.Scrollbar(self.training_manager)
        self.x_scrollbar.grid(row=6, column=5, rowspan=4, sticky='ns')

        # Create an x column Listbox
        self.xcolumn_listbox = tk.Listbox(self.training_manager, height=4, width=15, yscrollcommand=self.x_scrollbar.set)
        self.xcolumn_listbox.grid(row=6, column=4, rowspan=4, sticky='nsew')

        # Configure the scrollbar to scroll x column Listbox
        self.x_scrollbar.config(command=self.xcolumn_listbox.yview)
        
        # Create a button to move selected items from the independent column Listbox to x column Listbox
        self.xmove_button = ttk.Button(self.training_manager, text="-->", command=lambda: self.move_items(self.ind_column_listbox, self.xcolumn_listbox, False, False))
        self.xmove_button.grid(row=7, column=3, padx=3)
        self.xmove_button.configure(width=2)

        # Create a button to move selected items from the x column Listbox to independent column Listbox
        self.xmove_back_button = ttk.Button(self.training_manager, text="<--", command=lambda: self.move_items(self.xcolumn_listbox, self.ind_column_listbox, False, False))
        self.xmove_back_button.grid(row=8, column=3, padx=3)
        self.xmove_back_button.configure(width=2)
        
        
        # Create a label for the dependent column Listbox
        self.dep_column_label = ttk.Label(self.training_manager, text="Dependent Variable:")
        self.dep_column_label.grid(row=10, column=0, columnspan=2)

        # Create a scrollbar for dependent column Listbox
        self.dep_scrollbar = ttk.Scrollbar(self.training_manager)
        self.dep_scrollbar.grid(row=11, column=1, rowspan=4, sticky='ns')

        # Create a dependent column Listbox
        self.dep_column_listbox = tk.Listbox(self.training_manager, height=4, width=15, yscrollcommand=self.dep_scrollbar.set)
        self.dep_column_listbox.grid(row=11, column=0, rowspan=4, sticky='nsew')

        # Configure the scrollbar to scroll the Listbox
        self.dep_scrollbar.config(command=self.dep_column_listbox.yview)
        
        # Create a label for predict
        self.ycolumn_label = ttk.Label(self.training_manager, text="Predict:")
        self.ycolumn_label.grid(row=11, column=4, columnspan=2, rowspan=2, pady=1, sticky='s')
        
        # Create a label for predict feature label selection
        self.pred_label = ttk.Label(self.training_manager, width=15)
        self.pred_label.grid(row=13, column=4, columnspan=2, rowspan=2, pady=1, sticky='n')
        
        # Create a button to move selected items from dependent column Listbox to predict label
        self.ymove_button = ttk.Button(self.training_manager, text="-->", command=lambda: self.move_items(self.dep_column_listbox, self.pred_label, True, False))
        self.ymove_button.grid(row=12, column=3, padx=3)
        self.ymove_button.configure(width=2)

        # Create a button to move selected items from predict label to dependent column Listbox
        self.ymove_back_button = ttk.Button(self.training_manager, text="<--", command=lambda: self.move_items(self.pred_label, self.dep_column_listbox, False, True))
        self.ymove_back_button.grid(row=13, column=3, padx=3)
        self.ymove_back_button.configure(width=2)
        
        # Create a label for displaying messages to user
        self.success_label = ttk.Label(self.training_manager, wraplength=300)
        self.success_label.grid(row=14, column=4, columnspan=4, pady=1)
        
        # Create a label for algorithm selection
        self.algorithm_label = ttk.Label(self.training_manager, text="Algorithm:")
        self.algorithm_label.grid(row=2, column=6, columnspan=2, pady=2, sticky="s")

        # Create a combobox for algorithm selection
        self.algorithm_combobox = ttk.Combobox(self.training_manager, width=13)
        self.algorithm_combobox.grid(row=3, column=6, columnspan=2, padx=3)
        # Bind the function to the combobox selection event
        self.algorithm_combobox.bind("<<ComboboxSelected>>", self.on_alg_combobox_select)
        
        # Populate the algorithms combobox with the algorithm names
        self.algorithm_combobox["values"] = self.algorithms
        self.algorithm_combobox.current(0)  # Set selection to first element
        
        # Create a label for algorithm method selection
        self.method_label = ttk.Label(self.training_manager, text="Method:")
        self.method_label.grid(row=5, column=6, columnspan=2, pady=2, sticky="s")
        #Disabled on default
        self.method_label.config(state="disabled")

        # Create a combobox for algorithm method selection
        self.method_combobox = ttk.Combobox(self.training_manager, width=13)
        self.method_combobox.grid(row=6, column=6, columnspan=2, padx=3)
        #Disabled on default
        self.method_combobox.config(state="disabled")
        
        # Create a label for data scaling
        self.scale_label = ttk.Label(self.training_manager, text="Scaling:")
        self.scale_label.grid(row=7, column=6, columnspan=2, pady=2, sticky="s")

        # Create a combobox for data scaling type
        self.scale_combobox = ttk.Combobox(self.training_manager, width=13)
        self.scale_combobox.grid(row=8, column=6, columnspan=2, padx=3, sticky="n")
        # Populate the data scaling type combobox
        self.scale_combobox["values"] = self.scale_types
        self.scale_combobox.set("")
        
        # Create a label for test size
        self.test_size_label = ttk.Label(self.training_manager, text="Test Size:")
        self.test_size_label.grid(row=9, column=6, sticky="e")

        # Create a combobox for test size
        self.test_size_combobox = ttk.Combobox(self.training_manager, width=5)
        self.test_size_combobox.grid(row=9, column=7, padx=1, pady=2)
        # Populate the test size combobox
        self.test_size_combobox["values"] = self.test_sizes
        self.test_size_combobox.set(20)
        
        # Create a slider for cluster number selection
        self.cluster_label = ttk.Label(self.training_manager, text="Clusters: 1")
        self.cluster_label.grid(row=10, column=6, columnspan=2, pady=2, sticky="s")
        
        self.cluster_slider = ttk.Scale(self.training_manager, from_=1, to=100, orient="horizontal", length=140)
        self.cluster_slider.grid(row=11, column=6, columnspan=2,)
        self.cluster_slider.bind("<B1-Motion>", self.handle_slider)
        self.cluster_slider.set(1)
                                  
        # Disable cluster GUI elements by default
        self.cluster_label.config(state="disabled")
        self.cluster_slider.config(state="disabled")
        
        # Create a button to train model
        self.start_button = ttk.Button(self.training_manager, text="Train Model", command=self.train_model)
        self.start_button.grid(row=12, column=6, columnspan=2, rowspan=3)

        
        self.training_manager.rowconfigure(1, minsize=7)
        self.training_manager.rowconfigure(4, minsize=7)
        self.training_manager.rowconfigure(14, minsize=25)
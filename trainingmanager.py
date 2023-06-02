from myimports import (
    sys, tk, ttk, filedialog, mysql, pd,
    create_engine, text, Integer, Text, String, DateTime, Boolean,
    sns, plt, Image, ImageTk,
    large_font, medium_font, small_bold, server_details, sqlalc_eng
)


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
            for column in columns:
                self.ind_column_listbox.insert(tk.END, column[0])
                self.dep_column_listbox.insert(tk.END, column[0])
                #column_names.append(column[0])
            
            #df = pd.DataFrame(rows, columns=column_names)
        
            query = f"SELECT * FROM `{selected_table}`"
        
            # Create SQLAlchemy engine
            engine = create_engine(sqlalc_eng)

            # Read the table data into a Pandas DataFrame
            self.current_dataframe = pd.read_sql_query(sql=text(query), con=engine.connect())
        
            # Close the SQLAlchemy engine
            engine.dispose()
        
            self.current_dataframe.info()
        
            # Generate a pairplot to quickly see how varaiables relate to one another
            pairplot = sns.pairplot(self.current_dataframe, kind= 'scatter')
            
            # Replace 'filename' with the desired name of your output file
            filename = "pairplot.jpg"
            pairplot.savefig(filename)
        
            # Set the backend to TkAgg
            #plt.switch_backend('TkAgg')
        
            # Display the plot
            # plt.show()
            # plt.waitforbuttonpress()
        
            # Load the image
            #image = Image.open("pairplot.jpg")
            #photo = ImageTk.PhotoImage(image)
        
            # load pairplot image to be displayed
            #image = PhotoImage(file="pairplot.jpg")
        
            self.change_image(self.canvas, filename)
        
            # Set the image to the label
            #view_window_label.config(image=photo)
            #view_window_label.image = photo
            
            self.dataframe_toolbar.selected_table = selected_table
            
            # Clear any existing options in the combobox
            self.dataframe_toolbar.column_combobox['values'] = ()

            # Add the column names as options to the combobox
            self.dataframe_toolbar.column_combobox['values'] = self.current_dataframe.columns.tolist()


            # Close the cursor and connection
            cursor.close()
            connection.close()
        
    # Function to change the image on the label
    def change_image(self, widget, new_image_path):
        new_image = Image.open(new_image_path)
        new_photo = ImageTk.PhotoImage(new_image)
    
         # Update the existing image item on the Canvas
        widget.itemconfig(self.image_item, image=new_photo)
    
        #widget.config(image=new_photo)
        widget.image = new_photo  # Keep a reference to the new image
    
        # Configure the Scrollbar to scroll the Canvas
        widget.config(scrollregion=widget.bbox("all"))
    
    def __init__(self, frame, canvas, image_item, current_dataframe, dataframe_toolbar):
        self.home_frame = frame
        self.canvas = canvas
        self.image_item = image_item
        self.current_dataframe = current_dataframe
        self.dataframe_toolbar = dataframe_toolbar

        # Create left and right frames
        self.training_manager = tk.Frame(self.home_frame, width=180, height=185, bg='purple')
        self.training_manager.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    
        # Create a label for the table selection
        self.table_label = ttk.Label(self.training_manager, text="Training Manager", font=large_font)
        self.table_label.grid(row=0, column=0, columnspan=2)
    
        # Create a label for the table selection
        self.table_label = ttk.Label(self.training_manager, text="Select a table:")
        self.table_label.grid(row=2, column=0, columnspan=2)

        # Create a combobox for table selection
        self.table_combobox = ttk.Combobox(self.training_manager)
        self.table_combobox.grid(row=3, column=0, columnspan=2)
        # Bind the function to the combobox selection event
        self.table_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # Create a label for the column selection
        self.ind_column_label = ttk.Label(self.training_manager, text="Select Independent Variables:")
        self.ind_column_label.grid(row=5, column=0, columnspan=2)

        # Create a scrollbar
        self.ind_scrollbar = ttk.Scrollbar(self.training_manager)
        self.ind_scrollbar.grid(row=6, column=1, sticky='ns')

        # Create a Listbox widget
        self.ind_column_listbox = tk.Listbox(self.training_manager, height=4, width=22, yscrollcommand=self.ind_scrollbar.set, selectmode=tk.MULTIPLE)
        self.ind_column_listbox.grid(row=6, column=0, padx=2, sticky='nsew')

        # Configure the scrollbar to scroll the Listbox
        self.ind_scrollbar.config(command=self.ind_column_listbox.yview)



        # Create a label for the column selection
        self.dep_column_label = ttk.Label(self.training_manager, text="Select dependent Variables:")
        self.dep_column_label.grid(row=8, column=0, columnspan=2)

        # Create a scrollbar
        self.dep_scrollbar = ttk.Scrollbar(self.training_manager)
        self.dep_scrollbar.grid(row=9, column=1, sticky='ns')

        # Create a Listbox widget
        self.dep_column_listbox = tk.Listbox(self.training_manager, height=4, width=22, yscrollcommand=self.dep_scrollbar.set)
        self.dep_column_listbox.grid(row=9, column=0, padx=2, sticky='nsew')

        # Configure the scrollbar to scroll the Listbox
        self.dep_scrollbar.config(command=self.dep_column_listbox.yview)

        self.training_manager.rowconfigure(1, minsize=10)
        self.training_manager.rowconfigure(4, minsize=10)
        self.training_manager.rowconfigure(7, minsize=10)


        # Create a combobox for column selection
        #column_combobox = ttk.Combobox(root)
        #column_combobox.grid(row=5, column=3, columnspan=2)
    
        def start_algorithm():
            selected_table = table_combobox.get()
            selected_columns = column_combobox.get()
            # Add code to start the machine learning algorithm with the selected table and columns

        # Create a button to start the algorithm
        self.start_button = ttk.Button(self.training_manager, text="Start Algorithm", command=start_algorithm)
        self.start_button.grid(row=10, column=0, columnspan=2)
    
from myimports import (
    sys, tk, ttk, filedialog, mysql, pd,
    create_engine, text, Integer, Text, String, DateTime, Boolean,
    sns, plt, Image, ImageTk,
    large_font, medium_font, small_bold, server_details, sqlalc_eng
)


class DataFrameToolbar:
            
    def on_column_combobox_select(self, event):
        selected_column = self.column_combobox.get()
    
        if selected_column:
            print("Column selected")
                    
    
    def show_tables(self):
        # Clear the table listbox
        self.table_listbox.delete(0, tk.END)
    
        # Connect to the MariaDB server
        connection = mysql.connect(**server_details)
    
        try:
        
            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()
        
            # Execute the query to fetch table names
            cursor.execute("SHOW TABLES")
        
            # Fetch all table names
            tables = cursor.fetchall()
        
            # Insert table names into the listbox
            for table in tables:
                self.table_listbox.insert(tk.END, table[0])
            
            # Populate the table combobox with the table names
            self.training_manager.table_combobox["values"] = [table[0] for table in tables]
        
            self.training_manager.table_combobox.set("")  # Clear the selection
    
        except mysql.Error as e:
            print(f"Error: {e}")
    
        finally:
            # Close the cursor and database connection
            cursor.close()
            connection.close()

    
    def __init__(self, frame, current_dataframe):
        self.home_frame = frame
        self.current_dataframe = current_dataframe
        self.selected_table = ""
        
        # Create tool bar frame
        self.dataframe_tool_bar = tk.Frame(self.home_frame, width=180, height=185)
        self.dataframe_tool_bar.grid(row=1, column=1, padx=5, pady=5)

        # Create a label for the table selection
        self.table_label = ttk.Label(self.dataframe_tool_bar, text="DataFrame Toolbar", font=large_font)
        self.table_label.grid(row=1, column=0, columnspan=3, pady=3, sticky="s")
        
        # Create a label for the table selection
        self.table_label = ttk.Label(self.dataframe_tool_bar, text="Table: "+self.selected_table)
        self.table_label.grid(row=2, column=0, columnspan=2)

        # Create a label for the table creation section
        self.create_label = ttk.Label(self.dataframe_tool_bar, text="Convert Data Types", font=medium_font)
        self.create_label.grid(row=3, column=0, columnspan=3)
        
        # Create a label for the table selection
        self.table_label = ttk.Label(self.dataframe_tool_bar, text="Select Column:")
        self.table_label.grid(row=2, column=0, columnspan=2)

        # Create a combobox for table selection
        self.column_combobox = ttk.Combobox(self.dataframe_tool_bar)
        self.column_combobox.grid(row=3, column=0, columnspan=2)
        # Bind the function to the combobox selection event
        self.column_combobox.bind("<<ComboboxSelected>>", self.on_column_combobox_select)

        
        # Create a button to create the table
        #self.create_table_button = ttk.Button(self.dataframe_tool_bar, text="Create Table from CSV", command=self.create_table)
        #self.create_table_button.grid(row=5, column=0, columnspan=3, sticky="n")

        # Create a label for the table creation section
        self.delete_label = ttk.Label(self.dataframe_tool_bar, text="Delete Table", font=medium_font)
        self.delete_label.grid(row=7, column=0, columnspan=3)

        

        # Create a label to display success message
        self.success_label = ttk.Label(self.dataframe_tool_bar)
        self.success_label.grid(row=12, column=0, columnspan=3, pady=5, sticky="n")


        self.dataframe_tool_bar.rowconfigure(2, minsize=10)
        self.dataframe_tool_bar.rowconfigure(6, minsize=10)
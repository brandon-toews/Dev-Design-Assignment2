from myimports import (
    sys, tk, ttk, filedialog, mysql, pd,
    create_engine, text, Integer, Text, String, DateTime, Boolean,
    sns, plt, Image, ImageTk,
    large_font, medium_font, small_bold, server_details, sqlalc_eng
)


class TableToolbar:
    
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

    def create_table(self):
    
        if self.table_name_entry.get():
    
            table_name = self.table_name_entry.get()
    
            file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if file_path:
                df = pd.read_csv(file_path)
            
                if 'Dt_Customer' in df:
                    # Convert the 'Dt_Customer' column to the correct datetime format
                    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d/%m/%Y')

                print("DataFrame loaded successfully!")
                print(df.head(5))
    
                try:
                    # Create SQLAlchemy engine
                    engine = create_engine(sqlalc_eng)
        
                    # Save the DataFrame into the newly created table
                    df.to_sql(
                        table_name,
                        engine,
                        index=False,
                        if_exists='replace',
                        chunksize=500,
                        dtype={
                            'ID': Integer,
                            'Year_Birth': Integer,
                            'Education': String(50),
                            'Marital_Status': String(50),
                            'Income': Integer,
                            'KidHome': Integer,
                            'TeenHome': Integer,
                            'Dt_Customer': DateTime,
                            'Regency': Integer,
                            'MntWines': Integer,
                            'MntFruits': Integer,
                            'MntMeatProducts': Integer,
                            'MntFishProducts': Integer,
                            'MntSweetProducts': Integer,
                            'MntGoldsProds': Integer,
                            'NumDealsPurchases': Integer,
                            'NumWebPurchases': Integer,
                            'NumCatalogPurchases': Integer,
                            'NumStorePurchases': Integer,
                            'NumWebVisitsMonth': Integer,
                            'AcceptedCmp3': Integer,
                            'AcceptedCmp4': Integer,
                            'AcceptedCmp5': Integer,
                            'AcceptedCmp1': Integer,
                            'AcceptedCmp2': Integer,
                            'Complain': Boolean,
                            'Z_CostContact': Integer,
                            'Z_Revenue': Integer,
                            'Response': Integer
                        }
                    )
        
                    # Show a success message to the user
                    self.success_label.config(text=f"Table '{table_name}' created successfully.", foreground="black", font=small_bold)
    
                except mysql.Error as e:
                    print(f"Error: {e}")
    
                finally:
                    # Close the cursor and database connection
                    #cursor.close()
                    #connection.close()
                    # Close the SQLAlchemy engine
                    engine.dispose()
                    self.table_name_entry.delete(0, tk.END)
                    self.show_tables()
                
        else:
            self.success_label.config(text="Must enter a table name!", foreground="red", font=small_bold)
        
        
    def delete_table(self):
    
        if self.table_listbox.curselection():
    
            selected_table = self.table_listbox.get(self.table_listbox.curselection())
    
            # Connect to the MariaDB server
            connection = mysql.connect(**server_details)
    
            try:
            
                # Create a cursor object to execute SQL queries
                cursor = connection.cursor()
        
                # Execute the query to delete the selected table
                cursor.execute(f"DROP TABLE `{selected_table}`")
        
                # Commit the changes to the database
                connection.commit()
        
                # Show a success message to the user
                self.success_label.config(text=f"Table '{selected_table}' deleted successfully.", foreground="black", font=small_bold)
    
            except mysql.Error as e:
                print(f"Error: {e}")
    
            finally:
                # Close the cursor and database connection
                cursor.close()
                connection.close()
                #Refresh table info
                self.show_tables()
                
    def quit_program(self):
        self.exit_flag.set(True)
        
    
    def __init__(self, frame, training_manager, exit_flag):
        self.home_frame = frame
        self.training_manager = training_manager
        self.exit_flag = exit_flag
        
        # Create tool bar frame
        self.table_tool_bar = tk.Frame(self.home_frame, width=180, height=185)
        self.table_tool_bar.grid(row=1, column=0, padx=5, pady=5)

        # Create a label for the table selection
        self.table_label = ttk.Label(self.table_tool_bar, text="Table Manager", font=large_font)
        self.table_label.grid(row=1, column=0, columnspan=3, pady=3, sticky="s")

        # Create a label for the table creation section
        self.create_label = ttk.Label(self.table_tool_bar, text="Create Table", font=medium_font)
        self.create_label.grid(row=3, column=0, columnspan=3)

        # Create an entry for table name
        self.table_name_label = ttk.Label(self.table_tool_bar, text="Name:")
        self.table_name_label.grid(row=4, column=0, padx=1, sticky="e")  # Place the label on the left (east)

        self.table_name_entry = ttk.Entry(self.table_tool_bar, width=17)
        self.table_name_entry.grid(row=4, column=1, columnspan=2, padx=1, sticky="w")  # Place the entry field next to the label


        # Create a button to create the table
        self.create_table_button = ttk.Button(self.table_tool_bar, text="Create Table from CSV", command=self.create_table)
        self.create_table_button.grid(row=5, column=0, columnspan=3, sticky="n")

        # Create a label for the table creation section
        self.delete_label = ttk.Label(self.table_tool_bar, text="Delete Table", font=medium_font)
        self.delete_label.grid(row=7, column=0, columnspan=3)

        # Create a label for the table selection
        self.table_label = ttk.Label(self.table_tool_bar, text="Select a table:")
        self.table_label.grid(row=8, column=0, columnspan=3)

        # Create a scrollbar 
        self.table_scrollbar = ttk.Scrollbar(self.table_tool_bar)
        self.table_scrollbar.grid(row=9, column=2, sticky='nsw')

        # Create a listbox to display table names
        self.table_listbox = tk.Listbox(self.table_tool_bar, height=4, width=22, yscrollcommand=self.table_scrollbar.set)
        self.table_listbox.grid(row=9, column=0, columnspan=2, padx=2, sticky='e')

        # Configure the scrollbar to scroll the Listbox
        self.table_scrollbar.config(command=self.table_listbox.yview)

        #Populate tables in database on startup
        self.show_tables()

        # Create a button to delete the selected table
        self.delete_button = ttk.Button(self.table_tool_bar, text="Delete Table", command=self.delete_table)
        self.delete_button.grid(row=10, column=0, columnspan=3, sticky="n")

        # Create a button to quit the program
        self.create_table_button = ttk.Button(self.table_tool_bar, text="Quit", command=self.quit_program)
        self.create_table_button.grid(row=11, column=0, columnspan=3, pady=3, sticky="s")

        # Create a label to display success message
        self.success_label = ttk.Label(self.table_tool_bar)
        self.success_label.grid(row=12, column=0, columnspan=3, pady=5, sticky="n")


        self.table_tool_bar.rowconfigure(2, minsize=10)
        self.table_tool_bar.rowconfigure(6, minsize=10)
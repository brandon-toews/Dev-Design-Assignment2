from myimports import (
    tk, ttk, pd, sns, plt, Image, ImageTk,
    large_font, medium_font, small_bold
)
class ViewWindow:
    
    # Function to change the image on the label
    def change_image(self, new_image_path):
        new_image = Image.open(new_image_path)
        new_photo = ImageTk.PhotoImage(new_image)
    
         # Update the existing image item on the Canvas
        self.canvas.itemconfig(self.image_item, image=new_photo)
    
        #widget.config(image=new_photo)
        self.canvas.image = new_photo  # Keep a reference to the new image
    
        # Configure the Scrollbar to scroll the Canvas
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def __init__(self, frame):
        self.home_frame = frame
        
        # Load the image
        self.image = Image.open("data_visualization_general.jpg")
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a Canvas widget
        self.canvas = tk.Canvas(self.home_frame, width=640, height=595)
        self.canvas.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        # Display the initial image on the Canvas
        self.image_item = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

        # Create a Scrollbar widget
        self.canvas_yscrollbar = tk.Scrollbar(self.home_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas_yscrollbar.grid(row=0, column=1, sticky='ns')

        # Create a Scrollbar widget
        self.canvas_xscrollbar = tk.Scrollbar(self.home_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas_xscrollbar.grid(row=1, column=0, sticky='we')

        # Configure the Canvas to use the Scrollbar
        self.canvas.config(yscrollcommand=self.canvas_yscrollbar.set, xscrollcommand=self.canvas_xscrollbar.set)
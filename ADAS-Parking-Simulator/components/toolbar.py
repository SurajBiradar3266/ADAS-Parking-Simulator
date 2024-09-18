import tkinter as tk

class Toolbar:
    """
    Creates a toolbar with buttons and vehicle coordinate display at the top and bottom of the main window.
    """
    def __init__(self, root, quit_app):
        """
        Initializes the Toolbar instance.
        
        Args:
            root (tk.Tk): The main application window.
            quit_app (function): The function to be called when the quit button is pressed.
        """
        self.root = root
        self.quit_app = quit_app
        
        # Create the toolbar frame at the top
        self.top_frame = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        # Create and add the quit button
        self.quit_button = tk.Button(self.top_frame, text="Quit", command=self.quit_app)
        self.quit_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a frame for vehicle coordinates at the bottom
        self.bottom_frame = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Create labels to display latitude and longitude
        self.lat_label = tk.Label(self.bottom_frame, text="Latitude: N/A", font=("Arial", 8))
        self.lon_label = tk.Label(self.bottom_frame, text="Longitude: N/A", font=("Arial", 8))
        

        self.lat_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.lon_label.pack(side=tk.LEFT, padx=5, pady=5)
          # Add status label to the bottom frame

        # Create and manage indicators using the Indicator subclass
        self.indicator_frame = tk.Frame(self.bottom_frame, bd=1, relief=tk.RAISED)
        self.indicator_frame.pack(side=tk.RIGHT, fill=tk.X)

        self.red_indicator = self.Indicator(self.indicator_frame, "Red", "Vehicle is reversing")
        self.yellow_indicator = self.Indicator(self.indicator_frame, "Yellow", "Vehicle is stopped")
        self.green_indicator = self.Indicator(self.indicator_frame, "Green", "Vehicle is moving forward")

        # Parking label
        self.ParkingStatus_frame = tk.Frame(self.bottom_frame, bd=1, relief=tk.RAISED)
        self.ParkingStatus_frame.pack(side=tk.RIGHT, fill=tk.X)
        self.ParkingStatus_label = tk.Label(self.ParkingStatus_frame, text="Status: Not Parked", font=("Arial", 8))  # New label
        self.ParkingStatus_label.pack(side=tk.RIGHT, padx=5, pady=5)


    def update_coordinates(self, latitude, longitude):
        """
        Updates the latitude and longitude display labels.
        
        Args:
            latitude (float): The current latitude of the vehicle.
            longitude (float): The current longitude of the vehicle.
        """
        self.lat_label.config(text=f"Latitude: {latitude:.6f}")
        self.lon_label.config(text=f"Longitude: {longitude:.6f}")

    def update_indicator(self, status):
        """
        Updates the vehicle status indicators (Red, Yellow, Green).
        
        Args:
            status (str): The status of the vehicle ("forward", "reverse", "stopped").
        """
        # Reset all indicators
        self.red_indicator.set_inactive()
        self.yellow_indicator.set_inactive()
        self.green_indicator.set_inactive()

        # Update the relevant indicator based on the vehicle status
        if status == "reverse":
            self.red_indicator.set_active()
        elif status == "stopped":
            self.yellow_indicator.set_active()
        elif status == "forward":
            self.green_indicator.set_active()

    def update_parking_status(self, is_parked):
        """
        Updates the parking status display on the toolbar.
        
        Args:
            is_parked (bool): True if the vehicle is parked, False otherwise.
        """
        status_text = "Parked" if is_parked else "Not Parked"
        # Assuming you have a label or another widget to display the parking status
        self.ParkingStatus_label.config(text=status_text)

    class Indicator:
        """
        A subclass to represent individual indicators (red, yellow, green) in the toolbar.
        """
        def __init__(self, parent, color, tooltip_text):
            """
            Initializes the indicator.

            Args:
                parent (tk.Frame): The parent frame where the indicator will be placed.
                color (str): The color of the indicator (Red, Yellow, Green).
                tooltip_text (str): The tooltip text when hovering over the indicator.
            """
            self.parent = parent
            self.color = color.lower()
            self.tooltip_text = tooltip_text
            self.is_active = False

            # Create the indicator as a canvas object
            self.canvas = tk.Canvas(parent, width=20, height=20, bg="lightgrey", highlightthickness=1, highlightbackground="black")
            self.canvas.pack(side=tk.LEFT, padx=5, pady=5)
            self.indicator_circle = self.canvas.create_oval(5, 5, 15, 15, fill="lightgrey")

            # Bind tooltip display to mouse events
            self.canvas.bind("<Enter>", self.show_tooltip)
            self.canvas.bind("<Leave>", self.hide_tooltip)

        def set_active(self):
            """
            Activates the indicator by setting it to the specified color.
            """
            self.canvas.itemconfig(self.indicator_circle, fill=self.color)
            self.is_active = True

        def set_inactive(self):
            """
            Deactivates the indicator by setting it to a grey color.
            """
            self.canvas.itemconfig(self.indicator_circle, fill="lightgrey")
            self.is_active = False

        def show_tooltip(self, event):
            """
            Displays a tooltip with the purpose of the indicator when hovering over it.
            
            Args:
                event (tk.Event): The event object from the bind function.
            """
            self.tooltip = tk.Toplevel(self.parent)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{event.x_root + 0}+{event.y_root -30}")
            label = tk.Label(self.tooltip, text=self.tooltip_text, background="yellow", relief="solid", borderwidth=1, font=("Arial", 8))
            label.pack()

        def hide_tooltip(self, event=None):
            """
            Hides the tooltip when the mouse leaves the indicator.
            
            Args:
                event (tk.Event, optional): The event object from the bind function. Defaults to None.
            """
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                self.tooltip = None

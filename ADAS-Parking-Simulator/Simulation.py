
import tkinter as tk
from PIL import Image, ImageTk
from components.toolbar import Toolbar
from components.road import Road
from components.gps_scale import GPSScale
from components.vehicle import Vehicle
from components.controller import Controller

class MySimulationGUI:
    """
    Main GUI class for the vehicle simulation application. It sets up the UI components
    and handles the simulation logic.
    """
    def __init__(self, root):
        """
        Initializes the MySimulationGUI instance.
        
        Args:
            root (tk.Tk): The main application window.
        """
        self.root = root
        self.root.title("Vehicle Simulator")
        self.root.geometry("1000x1000")  # Set initial window size
        # Maximize the window
         # Maximize the window
        # self.maximize_window()
        # Initialize position and scale_lines
        self.scale_lines = []  # Initialize scale_lines here

        # Create the toolbar
        self.toolbar = Toolbar(root, root.quit)

        # Create a separate canvas for GPS scaling on the root window
        self.gps_canvas = tk.Canvas(root, bg="lightgrey", width=150)
        self.gps_canvas.pack(side=tk.RIGHT, fill="both", expand=True,)

        # Create a separate canvas for road and vehicle objects
        self.object_canvas = tk.Canvas(self.gps_canvas, bg="white", width=140)
        self.object_canvas.pack(side=tk.RIGHT, fill="both", expand=True, padx=30, pady=30)

        # Create Road, Vehicle, and GPS Scale instances
        self.vehicle = Vehicle(self, self.object_canvas)
        self.road = Road(self)
        self.gps_scale = GPSScale(self)

        # Position vehicle on the road
        self.position_vehicle_on_road()

        # Create VehicleTracking instance and pass the Toolbar instance
        self.vehicle_tracking = Vehicle.VehicleTracking(self.vehicle, self.toolbar)

        # Create Controller instance and pass the root window
        self.controller = Controller(self.vehicle, self.root)

        # Bind window resize event to update UI components
        self.root.bind("<Configure>", self.on_resize)

    # def maximize_window(self):
    #     """
    #     Maximizes the window on Unix-based systems by setting geometry to screen size.
    #     """
    #     self.root.update_idletasks()  # Ensure window size is updated
    #     screen_width = self.root.winfo_screenwidth()
    #     screen_height = self.root.winfo_screenheight()
    #     self.root.geometry(f"{screen_width}x{screen_height}+0+0")  # Set to full screen

    def position_vehicle_on_road(self):
        """
        Positions the vehicle on the road based on the road's dimensions.
        """
        road_top, road_bottom = self.road.get_boundaries()

        # Calculate the initial position of the vehicle
        initial_x = (self.gps_canvas.winfo_width() - self.vehicle.vehicle_width) // 2
        initial_y = (road_top + road_bottom - self.vehicle.vehicle_width) // 2

        # Set vehicle position
        # self.vehicle.set_position(initial_x, initial_y)
        self.object_canvas.tag_raise(self.vehicle.image_id)

    def on_resize(self, event):
        """
        Handles window resize events to update the road and GPS scale.
        
        Args:
            event (tk.Event): The resize event.
        """
        self.road.create_road()
        self.gps_scale.create_gps_scale()
        self.position_vehicle_on_road()

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = MySimulationGUI(root)
    root.mainloop()



import math
from PIL import Image, ImageTk
import tkinter as tk
import json
import datetime

class Vehicle:
    """
    Represents a vehicle in the simulation. It handles the display of the vehicle
    on the canvas and integrates with the VehicleTracking class to calculate GPS coordinates.
    """
    def __init__(self, parent, canvas):
        """
        Initializes the Vehicle instance.
        
        Args:
            parent (MySimulationGUI): The parent GUI instance.
            canvas (tk.Canvas): The canvas where the vehicle image will be drawn.
        """
        self.parent = parent
        self.canvas = canvas
        self.vehicle_x = 10
        self.vehicle_y = 360
        self.vehicle_width = 60  # Width of the vehicle image
        self.angle = 0  # Current rotation angle of the vehicle
        self.speed = 10  # Movement speed

        # Load and resize the vehicle image
        self.original_image = Image.open("images/MyCar.png")  # Path to vehicle image
        self.original_image = self.original_image.resize((self.original_image.width // 15, self.original_image.height // 15), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.original_image)
        self.image_id = self.canvas.create_image(self.vehicle_x, self.vehicle_y, anchor="n", image=self.photo)

        # Parking slots (define as needed)
        self.parking_slots = [
            {'x1': 500, 'y1': 0, 'x2': 600, 'y2': 100},
            {'x1': 500, 'y1': 120, 'x2': 600, 'y2': 220},
            # Add more slots if needed
        ]

    def rotate_vehicle(self, direction):
        """
        Rotates the vehicle image to the left or right.
        
        Args:
            direction (str): 'left' or 'right' to rotate the vehicle in the respective direction.
        """
        if direction == "left":
            self.angle -= 10  # Rotate 10 degrees to the left
        elif direction == "right":
            self.angle += 10  # Rotate 10 degrees to the right

        # Rotate the image using the updated angle
        rotated_image = self.original_image.rotate(self.angle, resample=Image.Resampling.BICUBIC, expand=True)

        # Update the photo and the canvas image with the new rotated image
        self.photo = ImageTk.PhotoImage(rotated_image)
        self.canvas.itemconfig(self.image_id, image=self.photo)

    def move_forward(self):
        """
        Moves the vehicle forward based on its current angle.
        """
        # Calculate the new position based on the angle
        radians = math.radians(self.angle)
        self.vehicle_x += self.speed * math.cos(radians)
        self.vehicle_y -= self.speed * math.sin(radians)  # Subtract because y-axis is inverted in Tkinter

        # Update the position on the canvas
        self.update_position_on_canvas()

    def move_backward(self):
        """
        Moves the vehicle backward based on its current angle.
        """
        # Calculate the new position based on the angle
        radians = math.radians(self.angle)
        self.vehicle_x -= self.speed * math.cos(radians)
        self.vehicle_y += self.speed * math.sin(radians)  # Add because y-axis is inverted in Tkinter

        # Update the position on the canvas
        self.update_position_on_canvas()

    def update_position_on_canvas(self):
        """
        Updates the vehicle's position on the canvas.
        """
        self.canvas.coords(self.image_id, self.vehicle_x, self.vehicle_y)
        self.parent.vehicle_tracking.update_coordinates()
        self.check_if_parked()  # Check if parked after updating the position

    def check_if_parked(self):
        """
        Checks if the vehicle is parked in a parking slot and updates the toolbar status.
        """
        is_parked = False
        for slot in self.parking_slots:
            if (slot['x1'] <= self.vehicle_x <= slot['x2'] and
                slot['y1'] <= self.vehicle_y <= slot['y2']):
                is_parked = True
                break

        if hasattr(self.toolbar, 'update_parking_status'):
            self.toolbar.update_parking_status(is_parked)

    class VehicleTracking:
        """
        Manages vehicle tracking, including updating vehicle coordinates and notifying the toolbar.
        """
        def __init__(self, vehicle, toolbar):
            self.vehicle = vehicle
            self.toolbar = toolbar
            self.movement = self.VehicleMovement()
            self.update_coordinates()

        def get_coordinates(self):
            latitude = self.vehicle.vehicle_y / 10.0
            longitude = self.vehicle.vehicle_x / 10.0
            return latitude, longitude

        def update_coordinates(self):
            latitude, longitude = self.get_coordinates()
            self.toolbar.update_coordinates(latitude, longitude)
            status = self.movement.get_vehicle_status(self.vehicle)
            self.toolbar.update_indicator(status)
            self.movement.logger.log_position(self.vehicle)

        class VehicleMovement:
            def __init__(self):
                self.previous_x = 0
                self.previous_y = 0
                self.logger = self.PositionLogger()

            def get_vehicle_status(self, vehicle):
                if vehicle.vehicle_x > self.previous_x:
                    status = "forward"
                elif vehicle.vehicle_x < self.previous_x:
                    status = "reverse"
                else:
                    status = "stopped"
                self.previous_x = vehicle.vehicle_x
                self.previous_y = vehicle.vehicle_y
                return status

            class PositionLogger:
                def __init__(self):
                    self.log_file = "vehicle_positions.json"

                def log_position(self, vehicle):
                    from datetime import datetime  # Ensure import is here
                    longitude = vehicle.vehicle_x / 10.0
                    latitude = vehicle.vehicle_y / 10.0
                    timestamp = datetime.now().isoformat()
                    position_data = {
                        "latitude": latitude,
                        "longitude": longitude,
                        "timestamp": timestamp
                    }
                    try:
                        with open(self.log_file, "a") as file:
                            json.dump(position_data, file)
                            file.write("\n")
                    except IOError as e:
                        print(f"Error writing to log file: {e}")

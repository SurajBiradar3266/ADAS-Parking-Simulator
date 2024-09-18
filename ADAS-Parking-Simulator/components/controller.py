import tkinter as tk

class Controller:
    """
    Manages vehicle control using keyboard input.
    """
    def __init__(self, vehicle, root):
        self.vehicle = vehicle
        self.root = root
        self.bind_keys()

    def bind_keys(self):
        """
        Binds keyboard events to vehicle control functions.
        """
        self.root.bind("<Up>", self.move_forward)    # Move forward
        self.root.bind("<Down>", self.move_backward)  # Move backward
        self.root.bind("<Left>", self.rotate_right)    # Rotate left
        self.root.bind("<Right>", self.rotate_left)  # Rotate right

    def move_forward(self, event):
        """
        Moves the vehicle forward based on its current angle.

        Args:
            event (tk.Event): The key press event.
        """
        self.vehicle.move_forward()

    def move_backward(self, event):
        """
        Moves the vehicle backward based on its current angle.

        Args:
            event (tk.Event): The key press event.
        """
        self.vehicle.move_backward()

    def rotate_left(self, event):
        """
        Rotates the vehicle to the left.

        Args:
            event (tk.Event): The key press event.
        """
        self.vehicle.rotate_vehicle("left")

    def rotate_right(self, event):
        """
        Rotates the vehicle to the right.

        Args:
            event (tk.Event): The key press event.
        """
        self.vehicle.rotate_vehicle("right")

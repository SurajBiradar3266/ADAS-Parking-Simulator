import tkinter as tk

class GPSScale:
    """
    Handles the drawing of the GPS scale on the canvas. It provides a visual representation
    of the coordinate system with latitude and longitude markings.
    """
    def __init__(self, parent):
        """
        Initializes the GPSScale instance.
        
        Args:
            parent (MySimulationGUI): The parent GUI instance.
        """
        self.parent = parent
        self.create_gps_scale()

    def create_gps_scale(self):
        """
        Draws the GPS scale on the canvas, including latitude and longitude markings.
        """
        # Remove previous scale lines
        for line in self.parent.scale_lines:
            self.parent.gps_canvas.delete(line)
        self.parent.scale_lines.clear()

        # Define colors and font size
        label_color = "#000000"  # Color for the coordinate labels
        dashline_color = "#D3D3D3"  # Color for the scale lines
        font_size = 8  # Font size for labels

        # Get the width and height of the GPS canvas
        width = self.parent.gps_canvas.winfo_width() - 10  # Padding adjustment
        height = self.parent.gps_canvas.winfo_height() - 10  # Padding adjustment

        # Draw horizontal scale (latitude) with "N" prefix
        for i in range(0, width + 1, 50):  # Adjust step size for decimal scaling
            line_id = self.parent.gps_canvas.create_line(i, 0, i, height, fill=dashline_color, dash=(4, 2), tags="gps_scale")
            lat_label = f"{i / 10:.1f}° N"
            label_id = self.parent.gps_canvas.create_text(i, 10, text=lat_label, anchor="n", fill=label_color, font=("Arial", font_size), tags="gps_scale")
            self.parent.scale_lines.extend([line_id, label_id])

        # Draw vertical scale (longitude) with "E" prefix
        for j in range(0, height + 1, 50):  # Adjust step size for decimal scaling
            line_id = self.parent.gps_canvas.create_line(0, j, width, j, fill=dashline_color, dash=(4, 2), tags="gps_scale")
            lon_label = f"{j / 10:.1f}° E"
            label_id = self.parent.gps_canvas.create_text(10, j, text=lon_label, angle=90, anchor="w", fill=label_color, font=("Arial", font_size), tags="gps_scale")
            self.parent.scale_lines.extend([line_id, label_id])

        # Ensure GPS scale lines are drawn beneath other elements
        self.parent.gps_canvas.tag_lower("gps_scale")

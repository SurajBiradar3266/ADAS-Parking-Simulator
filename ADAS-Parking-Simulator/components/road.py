# import tkinter as tk

# class Road:
#     """
#     Represents the road on the canvas. It draws the road and road markings.
#     """
#     def __init__(self, parent):
#         """
#         Initializes the Road instance.
        
#         Args:
#             parent (MySimulationGUI): The parent GUI instance.
#         """
#         self.parent = parent
#         self.road_color = "#1d1813"  # Realistic road color
#         self.line_color = "#FFFFFF"  # Color for road markings (lines)
#         self.line_distance_from_edge = 20  # Distance from the top and bottom edges of the road
#         self.road_top = 0
#         self.road_bottom = 0
#         self.create_road()

#     def create_road(self):
#         """
#         Draws both horizontal and vertical roads with road markings on the canvas.
#         Removes the intersection patch where edge lines cross each other.
#         """
#         width = self.parent.gps_canvas.winfo_width()
#         height = self.parent.gps_canvas.winfo_height()
        
#         # Access the vehicle width from the Vehicle instance
#         vehicle_width = self.parent.vehicle.vehicle_width

#         # Horizontal Road
#         self.road_top = height // 2 - vehicle_width
#         self.road_bottom = height // 2 + vehicle_width

#         # Clear previous road and lines
#         self.parent.object_canvas.delete("road")
#         self.parent.object_canvas.delete("road_lines")

#         # Draw the horizontal road rectangle
#         self.parent.object_canvas.create_rectangle(
#             0, self.road_top, width, self.road_bottom,
#             fill=self.road_color, outline=self.road_color, tags="road"
#         )

#         # Draw white lines marking the edges of the horizontal road
#         intersection_x1 = width // 2 - vehicle_width // 2
#         intersection_x2 = width // 2 + vehicle_width // 2

#         self.parent.object_canvas.create_line(
#             0, self.road_top + self.line_distance_from_edge,
#             intersection_x1, self.road_top + self.line_distance_from_edge,
#             fill=self.line_color, width=2, tags="road_lines"
#         )
#         self.parent.object_canvas.create_line(
#             intersection_x2, self.road_top + self.line_distance_from_edge,
#             width, self.road_top + self.line_distance_from_edge,
#             fill=self.line_color, width=2, tags="road_lines"
#         )
#         self.parent.object_canvas.create_line(
#             0, self.road_bottom - self.line_distance_from_edge,
#             intersection_x1, self.road_bottom - self.line_distance_from_edge,
#             fill=self.line_color, width=2, tags="road_lines"
#         )
#         self.parent.object_canvas.create_line(
#             intersection_x2, self.road_bottom - self.line_distance_from_edge,
#             width, self.road_bottom - self.line_distance_from_edge,
#             fill=self.line_color, width=2, tags="road_lines"
#         )

#         # Vertical Road
#         road_left = width // 2 - vehicle_width
#         road_right = width // 2 + vehicle_width
#         intersection_y1 = self.road_top + vehicle_width // 2
#         intersection_y2 = self.road_bottom - vehicle_width // 2

#         # Draw the vertical road rectangle
#         self.parent.object_canvas.create_rectangle(
#             road_left, 0, road_right, height,
#             fill=self.road_color, outline=self.road_color, tags="road"
#         )

#         # Draw white lines marking the edges of the vertical road
#         self.parent.object_canvas.create_line(
#             road_left + self.line_distance_from_edge, 0,
#             road_left + self.line_distance_from_edge, intersection_y1,
#             fill=self.line_color, width=2, tags="road_lines"
#         )
#         self.parent.object_canvas.create_line(
#             road_left + self.line_distance_from_edge, intersection_y2,
#             road_left + self.line_distance_from_edge, height,
#             fill=self.line_color, width=2, tags="road_lines"
#         )
#         self.parent.object_canvas.create_line(
#             road_right - self.line_distance_from_edge, 0,
#             road_right - self.line_distance_from_edge, intersection_y1,
#             fill=self.line_color, width=2, tags="road_lines"
#         )
#         self.parent.object_canvas.create_line(
#             road_right - self.line_distance_from_edge, intersection_y2,
#             road_right - self.line_distance_from_edge, height,
#             fill=self.line_color, width=2, tags="road_lines"
#         )

#         # Cover the intersection area where the edge lines cross
#         self.parent.object_canvas.create_rectangle(
#             road_left + self.line_distance_from_edge, self.road_top + self.line_distance_from_edge,
#             road_right - self.line_distance_from_edge, self.road_bottom - self.line_distance_from_edge,
#             fill=self.road_color, outline=self.road_color, tags="road"
#         )

    # def get_boundaries(self):
    #     """
    #     Gets the boundaries of the road.
        
    #     Returns:
    #         tuple: (road_top, road_bottom)
    #     """
    #     width = self.parent.gps_canvas.winfo_width()
    #     height = self.parent.gps_canvas.winfo_height()
    #     vehicle_width = self.parent.vehicle.vehicle_width
    #     self.road_top = height // 2 - vehicle_width
    #     self.road_bottom = height // 2 + vehicle_width
    #     return self.road_top, self.road_bottom
import tkinter as tk

class Road:
    """
    Represents the road on the canvas. It draws the road, road markings, and parking slots.
    """
    def __init__(self, parent):
        """
        Initializes the Road instance.
        
        Args:
            parent (MySimulationGUI): The parent GUI instance.
        """
        self.parent = parent
        self.road_color = "#1d1813"  # Realistic road color
        self.line_color = "#FFFFFF"  # Color for road markings (lines)
        self.parking_slot_color = "#2e2a28"  # Slightly lighter color for parking slots
        self.parking_line_color = "#FFFF00"  # Yellow color for parking slot lines
        self.line_distance_from_edge = 20  # Distance from the top and bottom edges of the road
        self.road_top = 0
        self.road_bottom = 0
        self.slot_width = 40  # Width of each parking slot
        self.slot_height = 80  # Height of each parking slot
        self.create_road()

    def create_road(self):
        """
        Draws both horizontal and vertical roads with road markings on the canvas.
        Removes the intersection patch where edge lines cross each other.
        Adds parking slots in the top-right block.
        """
        width = self.parent.gps_canvas.winfo_width()
        height = self.parent.gps_canvas.winfo_height()
        
        # Access the vehicle width from the Vehicle instance
        vehicle_width = self.parent.vehicle.vehicle_width

        # Clear previous road and lines
        self.parent.object_canvas.delete("road")
        self.parent.object_canvas.delete("road_lines")
        self.parent.object_canvas.delete("parking_slot")  # Clear existing parking slots
        self.parent.object_canvas.delete("parking_slot_line")  # Clear existing parking slot lines

        # Draw the horizontal road rectangle
        self.parent.object_canvas.create_rectangle(
            0, self.road_top, width, self.road_bottom,
            fill=self.road_color, outline=self.road_color, tags="road"
        )

        # Draw white lines marking the edges of the horizontal road
        intersection_x1 = width // 2 - vehicle_width // 2
        intersection_x2 = width // 2 + vehicle_width // 2

        self.parent.object_canvas.create_line(
            0, self.road_top + self.line_distance_from_edge,
            intersection_x1, self.road_top + self.line_distance_from_edge,
            fill=self.line_color, width=2, tags="road_lines"
        )
        self.parent.object_canvas.create_line(
            intersection_x2, self.road_top + self.line_distance_from_edge,
            width, self.road_top + self.line_distance_from_edge,
            fill=self.line_color, width=2, tags="road_lines"
        )
        self.parent.object_canvas.create_line(
            0, self.road_bottom - self.line_distance_from_edge,
            intersection_x1, self.road_bottom - self.line_distance_from_edge,
            fill=self.line_color, width=2, tags="road_lines"
        )
        self.parent.object_canvas.create_line(
            intersection_x2, self.road_bottom - self.line_distance_from_edge,
            width, self.road_bottom - self.line_distance_from_edge,
            fill=self.line_color, width=2, tags="road_lines"
        )

        # Vertical Road
        road_left = width // 2 - vehicle_width
        road_right = width // 2 + vehicle_width
        intersection_y1 = self.road_top + vehicle_width // 2
        intersection_y2 = self.road_bottom - vehicle_width // 2

        # Draw the vertical road rectangle
        self.parent.object_canvas.create_rectangle(
            road_left, 0, road_right, height,
            fill=self.road_color, outline=self.road_color, tags="road"
        )

        # Draw white lines marking the edges of the vertical road
        self.parent.object_canvas.create_line(
            road_left + self.line_distance_from_edge, 0,
            road_left + self.line_distance_from_edge, intersection_y1,
            fill=self.line_color, width=2, tags="road_lines"
        )
        self.parent.object_canvas.create_line(
            road_left + self.line_distance_from_edge, intersection_y2,
            road_left + self.line_distance_from_edge, height,
            fill=self.line_color, width=2, tags="road_lines"
        )
        self.parent.object_canvas.create_line(
            road_right - self.line_distance_from_edge, 0,
            road_right - self.line_distance_from_edge, intersection_y1,
            fill=self.line_color, width=2, tags="road_lines"
        )
        self.parent.object_canvas.create_line(
            road_right - self.line_distance_from_edge, intersection_y2,
            road_right - self.line_distance_from_edge, height,
            fill=self.line_color, width=2, tags="road_lines"
        )

        # Cover the intersection area where the edge lines cross
        self.parent.object_canvas.create_rectangle(
            road_left + self.line_distance_from_edge, self.road_top + self.line_distance_from_edge,
            road_right - self.line_distance_from_edge, self.road_bottom - self.line_distance_from_edge,
            fill=self.road_color, outline=self.road_color, tags="road"
        )

        # Add parking slots in the top-right block
        self.create_parking_slots(width, height)


    def create_parking_slots(self, width, height):
        """
        Adds parking slots in the top-right block of the road.
        """
        slot_x_start = width // 2 + 100  # Start parking area a bit to the right of the road
        slot_y_start = height // 2 - 200  # Start parking area a bit above the road

        # Draw parking slots in the top-right block
        for i in range(5):  # Add 5 parking slots
            slot_x = slot_x_start + (self.slot_width + 30) * i  # Gap of 10 pixels between slots
            slot_y = slot_y_start
            self.parent.object_canvas.create_rectangle(
                slot_x, slot_y, slot_x + self.slot_width+30, slot_y + self.slot_height+30,
                fill=self.parking_slot_color, outline=self.parking_line_color, width=2, tags="parking_slot"
            )
            self.parent.object_canvas.create_line(
                slot_x, slot_y, slot_x, slot_y + self.slot_height+30,
                fill=self.parking_line_color, width=2, tags="parking_slot_line"
            )
            self.parent.object_canvas.create_line(
                slot_x + self.slot_width+30, slot_y, slot_x + self.slot_width+30, slot_y + self.slot_height+30,
                fill=self.parking_line_color, width=2, tags="parking_slot_line"
            )

    def get_boundaries(self):
        """
        Gets the boundaries of the road.
        
        Returns:
            tuple: (road_top, road_bottom)
        """
        width = self.parent.gps_canvas.winfo_width()
        height = self.parent.gps_canvas.winfo_height()
        vehicle_width = self.parent.vehicle.vehicle_width
        self.road_top = height // 2 - vehicle_width
        self.road_bottom = height // 2 + vehicle_width
        return self.road_top, self.road_bottom
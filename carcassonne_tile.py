""" File: carcassonne_tile.py
    Author: Colton Patch
    Course: CSC 120
    Purpose: Define the CarcassonneTile class.
"""
class CarcassonneTile:
    """ This class represents a single tile in the game carcassonne. It
        contains information about what occupies each edge of the tile, as
        well as whether or not the tile contains a crossroads.

        The constructor builds a tile, and it is passed a string
        describing what is in each edge ('city', 'grass', or 'grass+road')
        as well as a boolean representing whether or not the tile contains
        a crossroads.

        set_connected_cites(cities):    Creates a tuple of cities that are
                                            connected.
        set_crossroad_edges(edges):     Creates a tuple of edges with roads
                                            that connect to a crossroads.
        get_edge(side):                 Returns information about what 
                                            occupies a given edge.
        edge_has_road(side):            Returns a boolean: True if the given 
                                            edge has a road, False if not.
        edge_has_city(side):            Returns a boolean: True if the given 
                                            edge has a city, False if not.
        has_crossroads():               Returns a boolean: True if the tile
                                            has a crossroads, False if not.
        road_get_connection(from_side): Given an edge which has a road,
                                            returns the side which that
                                            road connects to.
        city_connects(sideA, sideB):    Returns a boolean: True if both
                                            given sides have cities that
                                            connect, False if not.
        rotate():                       Returns a new tile, which is the
                                            original rotated 90 degrees
                                            clockwise.
    """
    def __init__(self, N, E, S, W, crossroad_edges=()):
        self._edge_info = {0:N, 1:E, 2:S, 3:W}
        self._crossroad_edges = crossroad_edges
        self._connect_cities = ()


    def set_connected_cities(self, cities):
        """ Given a tuple of integers representing edges which have cities
            that are connected, this function sets the _connect_cities 
            field to that tuple
        """
        self._connect_cities = cities

    def get_edge(self, side):
        """ Returns info about the given ledge. Can be either 'grass', 'city',
            or 'grass+road'.
        """
        return self._edge_info[side]

    def edge_has_road(self, side):
        """ Returns True if the given edge has a road
        """
        return self._edge_info[side] == "grass+road"

    def edge_has_city(self, side):
        """ Returns True if the given edge has a city
        """
        return self._edge_info[side] == "city"

    def has_crossroads(self):
        """ Returns True if the tile has a crossroads.
        """
        return self._crossroad_edges != ()

    def road_get_connection(self, from_side):
        """ Given a side that has a road, returns an integer representing
            the other side that road connects to: 0=N, 1=E, 2=S, 3=W,
            returns -1 if the tile has a crossroads.
        """
        if from_side in self._crossroad_edges:
            return -1
        for edge, value in self._edge_info.items():
            if edge != from_side:
                if value == "grass+road":
                    return edge

    def city_connects(self, sideA, sideB):
        """ Given two sides, returns True if both sides contain cities
            that are connected.
        """
        if sideA == sideB:
            return True
        if sideA in self._connect_cities and sideB in self._connect_cities:
            return True
        return False

    def rotate(self):
        """ This function rotates a tile clockwise.
            Return Value: A new rotated tile object.
        """
        new_crossroads = self._rotate_values(self._crossroad_edges)
        rotated_tile = CarcassonneTile(self._edge_info[3], self._edge_info[0],\
            self._edge_info[1], self._edge_info[2], new_crossroads)
        new_cities = self._rotate_values(self._connect_cities)
        rotated_tile.set_connected_cities(new_cities)
        return rotated_tile

    def _rotate_values(self, vals):
        """ This function takes a tuple of values from 0 to 3 and rotates them:
            3 becomes 0, 0 becomes 1, etc.
            Return Value: A new rotated tuple.
        """
        rotated_vals = []
        for edge in vals:
            if edge == 3:
                rotated_vals.append(0)
            else:
                rotated_vals.append(edge + 1)
        return tuple(rotated_vals)


#  creating all the tiles to be used in the game   
tile01 = CarcassonneTile("city", "grass+road", "grass", "grass+road")
tile02 = CarcassonneTile("city", "city", "grass", "city")
tile02.set_connected_cities((0, 1, 3))
tile03 = CarcassonneTile("grass+road", "grass+road", "grass+road",\
    "grass+road", (0,1,2,3))
tile04 = CarcassonneTile("city", "grass+road", "grass+road", "grass")
tile05 = CarcassonneTile("city", "city", "city", "city")
tile05.set_connected_cities((0,1,2,3))
tile06 = CarcassonneTile("grass+road", "grass", "grass+road", "grass")
tile07 = CarcassonneTile("grass", "city", "grass", "city")
tile08 = CarcassonneTile("grass", "city", "grass", "city")
tile08.set_connected_cities((1,3))
tile09 = CarcassonneTile("city", "city", "grass", "grass")
tile09.set_connected_cities((0,1))
tile10 = CarcassonneTile("grass", "grass+road", "grass+road", "grass+road",\
    (1,2,3))
tile11 = CarcassonneTile("city", "grass+road", "grass+road", "city")
tile11.set_connected_cities((0,3))
tile12 = CarcassonneTile("city", "grass", "grass+road", "grass+road")
tile13 = CarcassonneTile("city", "grass+road", "grass+road", "grass+road", \
    (1,2,3))
tile14 = CarcassonneTile("city", "city", "grass", "grass")
tile15 = CarcassonneTile("grass", "grass", "grass+road", "grass+road",)
tile16 = CarcassonneTile("city", "grass", "grass", "grass")

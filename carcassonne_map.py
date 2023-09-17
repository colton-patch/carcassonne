""" File: carcassonne_map.py
    Author: Colton Patch
    Course: CSC 120
    Purpose: Define the CarcassonneMap class.
"""
import carcassonne_tile

class CarcassonneMap:
    """ This class represents a map of tiles in the Carcassone game.

        The constructor builds a starting map, which contains tile01
        at the location (0,0).

        get_all_coords():                        Returns a set of all the 
                                                    coordinates occupied by a
                                                    tile on the map.
        find_map_border():                      Returns a set of all the 
                                                    empty coordinates that 
                                                    border tiles on the map.
        get(x,y):                               Returns the tile object 
                                                    located at the given 
                                                    coordinates.
        add(x,y, tile):                         Places a given tile at the 
                                                    given location.
                                                    Returns a boolean 
                                                    indicating whether or not
                                                    the tile could be 
                                                    placed successfully.
        trace_road_one_direction(x,y, side):    Traces a road across multiple
                                                    tiles and returns an array
                                                    representing the path of 
                                                    the road in the given
                                                    direction.
        trace_road_one_direction(x,y, side):    Traces the entire path of a
                                                    road in both directions.
                                                    Returns an array
                                                    representing the full path
                                                    of the road from end to
                                                    end. The direction it 
                                                    traces is dependent on 
                                                    the given side
        trace_city(x,y, side):                  Traces the entire city
                                                    connected to a given
                                                    starting point. Returns
                                                    a boolean representing
                                                    whether or not the city
                                                    is complete, as well as 
                                                    a set of all the locations
                                                    of the city.
    """
    def __init__(self):
        self._tile_coords = {}
        self._tile_coords[(0,0)] = carcassonne_tile.tile01
        # The following establishes what direction an adjacent tile 
        # would be to each edge.
        self._adjacent_coords = {0:(0,1), 1:(1,0), 2:(0,-1), 3:(-1,0)}


    def get_all_coords(self):
        """ This function returns a set of all the coordinates on the map
            occupied by a tile.
        """
        coords = set()
        for pair in self._tile_coords:
            coords.add(pair)
        return coords

    def find_map_border(self):
        """ This function returns a set of all the coordinates that border
            the existing map of tiles.
        """
        border = set()
        coords = self.get_all_coords()
        for pair in coords:
            for i in range(-1, 2, 2):
                horizontal_tile = (pair[0] + i, pair[1])
                vertical_tile = (pair[0], pair[1] + i)
                if horizontal_tile not in coords:
                    border.add(horizontal_tile)
                if vertical_tile not in coords:
                    border.add(vertical_tile)
        return border

    def get(self, x,y):
        """ This function returns the tile occupying
            the given coordinates.
        """
        if (x,y) not in self._tile_coords:
            return None
        return self._tile_coords[(x,y)]

    def add(self, x,y, tile, confirm=True, tryOnly=False):
        """ This function adds a given tile to a given (x,y) coordinates.
            If confirm is set to True and the tile could not be added to 
            the location, the function returns False. Otherwise, it returns
            True.
            Arguments:  x,y are integer coordinates; the location to place the
                            tile.
                        tile is the tile object to be placed.
                        confirm is a boolean indicating whether or not the
                            function should check if it is legal to place
                            the tile in the given location.
                        tryOnly is a boolean indicating if the function should
                            only check if a move is possible or actually add
                            the tile to the map.
            Return Value:   A boolean indicating whether or not the move could
                                be made successfully.
        """
        if not confirm:
            self._tile_coords[(x,y)] = tile
            return True
        if (x,y) not in self.find_map_border():
            return False

        valid = True
        for edge, direction in self._adjacent_coords.items():
            adjacent = (x + direction[0], y + direction[1])
            adjacent_edge = (edge + 2) % 4
            if adjacent in self._tile_coords:
                adjacent_tile = self._tile_coords[adjacent]
                if adjacent_tile.get_edge(adjacent_edge) != \
                tile.get_edge(edge):
                    valid = False

        if not valid:
            return False
        if not tryOnly:
            self._tile_coords[(x,y)] = tile
        return True


    def trace_road_one_direction(self, x,y, side):
        """ This function finds the entire path that a road takes starting
            at a given location, moving in the direction of a given side.
            Arguments:  x,y is an ordered pair representing the starting
                            location.
                        side is an integer representing the side of the tile 
                            that the function will start tracing the road
                            towards.
            Return Value:   An array of tuples. Each tuple contains
                                information about a single tile in
                                the path that was traced: its coordinates,
                                the side from where the road enters the tile,
                                and the side from where the road exits the
                                tile.
        """
        start_side = side
        direction = self._adjacent_coords[side]
        next_tile_coords = (x + direction[0], y + direction[1])
        retval = []
        while next_tile_coords in self._tile_coords:
            next_tile = self._tile_coords[next_tile_coords]
            road_start_edge = (side + 2) % 4
            side = next_tile.road_get_connection(road_start_edge)

            retval.append(next_tile_coords + (road_start_edge,) + (side,))
            if side == -1:
                break
            if next_tile_coords == (x,y):
                if side == start_side:
                    break

            direction = self._adjacent_coords[side]
            next_tile_coords = (next_tile_coords[0] + direction[0], 
                next_tile_coords[1] + direction[1])

        return retval


    def trace_road(self, x,y, side):
        """ This function traces an entire road in both directions, returning
            its full path.
            Arguments:  x,y is an ordered pair representing the starting
                            location.
                        side is an integer representing the side that the path
                            should be moving towards.
            Return Value:   An array of tuples. Each tuple contains
                                information about a single tile in
                                the path that was traced: its coordinates,
                                the side from where the road enters the tile,
                                and the side from where the road exits the
                                tile.
        """
        start_tile = self._tile_coords[(x,y)]
        connecting_side = start_tile.road_get_connection(side)
        second_half = self.trace_road_one_direction(x,y, side)
        if second_half != []:
            if second_half[-1] == (x,y, connecting_side, side):
                return second_half
        if connecting_side == -1:
            return [(x,y, connecting_side, side)] + second_half

        first_half = self.trace_road_one_direction(x,y, connecting_side)
        first_half.reverse()
        for i in range(len(first_half)):
            cur = first_half[i]
            new_tuple = (cur[0], cur[1], cur[3], cur[2])
            first_half[i] = new_tuple
        return first_half + [(x,y, connecting_side, side)] + second_half


    def trace_city(self, x,y, side):
        """ This function creates a list of every location in a city that
            connects to a given starting point.
            Arguments:  x,y is an ordered pair representing the starting
                            location.
                        side is an integer representing which edge of the
                            tile the starting location is at.
            Return Value:   A boolean representing whether or not the city
                                is completed, and a set of every location
                                in the city. Each location is a tuple in the
                                format (x, y, side).
        """
        city_set = {(x,y, side)}
        city_complete = True
        TODO = {(x,y, side)}
        while len(TODO) != 0:
            TODO_dup = list(TODO)
            for location in TODO_dup:
                tile_x = location[0]
                tile_y = location[1]
                tile = self._tile_coords[(tile_x, tile_y)]

                current_edge = location[2]
                edges = [0, 1, 2, 3]
                edges.remove(current_edge)
                for edge in edges:
                    if tile.city_connects(current_edge, edge):
                        if (tile_x, tile_y, edge) not in city_set:
                            city_set.add((tile_x, tile_y, edge))
                            TODO.add((tile_x, tile_y, edge))

                neighbor_direction = self._adjacent_coords[current_edge]
                neighbor_x = tile_x + neighbor_direction[0]
                neighbor_y = tile_y + neighbor_direction[1]
                if (neighbor_x, neighbor_y) in self._tile_coords:
                    neighbor_edge = (current_edge + 2) % 4
                    if (neighbor_x, neighbor_y, neighbor_edge) not in city_set:
                        city_set.add((neighbor_x, neighbor_y, neighbor_edge))
                        TODO.add((neighbor_x, neighbor_y, neighbor_edge))
                else:
                    city_complete = False
                TODO.remove(location)
        return (city_complete, city_set)


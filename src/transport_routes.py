"""
This module contains the implementation of the public transport route management system.

The system provides efficient operations for:
- Adding and removing routes
- Adding and removing stops from routes
- Querying routes by stop
- Querying stops in a route

All operations are designed to be O(1) time complexity using a bi-directional
mapping between routes and stops.
"""
from typing import Set, Dict, List
from dataclasses import dataclass

@dataclass(frozen=True)  # Make the class immutable and hashable
class Stop:
    id: str
    name: str
    
    def __hash__(self):
        return hash(self.id)  # Hash based on ID only
        
    def __eq__(self, other):
        if not isinstance(other, Stop):
            return False
        return self.id == other.id  # Compare based on ID only

class TransportRouteSystem:
    """
    A system for managing public transport routes and their stops.
    Uses bi-directional mapping for efficient querying and updates.
    
    Time Complexity:
    - Adding/removing routes: O(1)
    - Adding/removing stops: O(1)
    - Querying routes by stop: O(1)
    
    Space Complexity: O(R * S) where R is number of routes and S is average stops per route
    """
    
    def __init__(self):
        self.routes: Dict[str, Set[Stop]] = {}  # route_id -> set of stops
        self.stop_to_routes: Dict[str, Set[str]] = {}  # stop_id -> set of route_ids

    def add_route(self, route_id: str) -> None:
        """
        Add a new route to the system.
        
        Args:
            route_id: Unique identifier for the route
            
        Raises:
            ValueError: If route_id already exists
        """
        if not route_id:
            raise ValueError("Route ID cannot be empty")
        if route_id in self.routes:
            raise ValueError(f"Route {route_id} already exists")
            
        self.routes[route_id] = set()

    def add_stop_to_route(self, route_id: str, stop: Stop) -> None:
        """
        Add a stop to an existing route.
        
        Args:
            route_id: ID of the route to add the stop to
            stop: Stop object to add
            
        Raises:
            ValueError: If route doesn't exist or stop is invalid
        """
        if not route_id or not stop or not stop.id:
            raise ValueError("Route ID and Stop (with ID) are required")
        if route_id not in self.routes:
            raise ValueError(f"Route {route_id} does not exist")
            
        # Add stop to route
        self.routes[route_id].add(stop)
        
        # Update reverse mapping
        if stop.id not in self.stop_to_routes:
            self.stop_to_routes[stop.id] = set()
        self.stop_to_routes[stop.id].add(route_id)

    def remove_stop_from_route(self, route_id: str, stop_id: str) -> None:
        """
        Remove a stop from a route.
        
        Args:
            route_id: ID of the route to remove the stop from
            stop_id: ID of the stop to remove
            
        Raises:
            ValueError: If route or stop doesn't exist
        """
        if not route_id or not stop_id:
            raise ValueError("Route ID and Stop ID are required")
        if route_id not in self.routes:
            raise ValueError(f"Route {route_id} does not exist")
            
        # Find and remove stop from route
        stop_to_remove = None
        for stop in self.routes[route_id]:
            if stop.id == stop_id:
                stop_to_remove = stop
                break
                
        if not stop_to_remove:
            raise ValueError(f"Stop {stop_id} not found in route {route_id}")
            
        self.routes[route_id].remove(stop_to_remove)
        
        # Update reverse mapping
        self.stop_to_routes[stop_id].remove(route_id)
        if not self.stop_to_routes[stop_id]:
            del self.stop_to_routes[stop_id]

    def get_routes_by_stop(self, stop_id: str) -> Set[str]:
        """
        Get all routes that contain a specific stop.
        
        Args:
            stop_id: ID of the stop to search for
            
        Returns:
            Set of route IDs that contain the stop
            
        Raises:
            ValueError: If stop_id is invalid
        """
        if not stop_id:
            raise ValueError("Stop ID cannot be empty")
            
        return self.stop_to_routes.get(stop_id, set())

    def get_stops_in_route(self, route_id: str) -> Set[Stop]:
        """
        Get all stops in a specific route.
        
        Args:
            route_id: ID of the route
            
        Returns:
            Set of Stop objects in the route
            
        Raises:
            ValueError: If route doesn't exist
        """
        if not route_id:
            raise ValueError("Route ID cannot be empty")
        if route_id not in self.routes:
            raise ValueError(f"Route {route_id} does not exist")
            
        return self.routes[route_id]